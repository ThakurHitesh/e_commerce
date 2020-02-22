from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Q
from api.serializers import UserSignUpSerializer, UserReadSerializer, UserLoginSerializer
from api.models import User, Buyer, Seller, Admin
from .services import get_request_data, response, error_response, inv_serializer_error_response
from api.redis import verify_otp
from api.constants import CONST_ERROR_MESSAGE_INCORRECT_OTP_KEY, CONST_ERROR_MESSAGE_EMAIL_NOT_PROVIDED_KEY, \
    CONST_ERROR_MESSAGE_INVALID_USER_KEY, CONST_ERROR_MESSAGE_EMAIL_OR_OTP_NOT_PROVIDED_KEY, \
    CONST_CHOICE_USER_TYPE_BUYER, CONST_CHOICE_USER_TYPE_SELLER, CONST_CHOICE_USER_TYPE_ADMIN


class UserSignUpAPIView(APIView):
    """
    sign up view for a new user
    """
    serializer_class = UserSignUpSerializer
    model = User

    def post(self, request):
        request_data = get_request_data(request, 'post')
        serializer = self.serializer_class(data=request_data)
        email = request_data["email"] if request_data.get("email") else None
        otp = request_data["otp"] if request_data.get("otp") else None
        if email:
            if verify_otp(email, otp):
                if serializer.is_valid():
                    user = serializer.save()
                    data = UserReadSerializer(user).data
                    data["auth-token"] = User.objects.filter(id=user.id)[0].create_auth_token()
                    return response(data, status.HTTP_201_CREATED)
                return inv_serializer_error_response(serializer, status.HTTP_400_BAD_REQUEST)
            return error_response(CONST_ERROR_MESSAGE_INCORRECT_OTP_KEY, status.HTTP_400_BAD_REQUEST)
        return error_response(CONST_ERROR_MESSAGE_EMAIL_NOT_PROVIDED_KEY, status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    """
    Login user using OTP
    """
    serializer_class = UserLoginSerializer
    model = User

    def post(self, request):
        request_data = get_request_data(request, 'post')
        email = request_data["email"] if request_data.get("email") else None
        otp = request_data["otp"] if request_data.get("otp") else None
        user_type = request_data["user_type"] if request_data.get("user_type") else None
        if email is not None and otp is not None and user_type is not None:
            if verify_otp(email, otp):
                user = User.objects.filter(Q(email=email), Q(user_type=user_type))
                if user.exists():
                    base_user = user[0]
                    if base_user.user_type == CONST_CHOICE_USER_TYPE_BUYER:
                        user = Buyer.objects.filter(id = base_user.id)[0]
                    if base_user.user_type == CONST_CHOICE_USER_TYPE_SELLER:
                        user = Seller.objects.filter(id = base_user.id)[0]
                    if base_user.user_type == CONST_CHOICE_USER_TYPE_ADMIN:
                        user = Admin.objects.filter(id = base_user.id)[0]
                    data = UserReadSerializer(user).data
                    data["auth-token"] = base_user.create_auth_token()
                    return response(data, status.HTTP_200_OK)
                return error_response(CONST_ERROR_MESSAGE_INVALID_USER_KEY, status.HTTP_400_BAD_REQUEST)
            return error_response(CONST_ERROR_MESSAGE_INCORRECT_OTP_KEY, status.HTTP_400_BAD_REQUEST)
        return error_response(CONST_ERROR_MESSAGE_EMAIL_OR_OTP_NOT_PROVIDED_KEY, status.HTTP_400_BAD_REQUEST)