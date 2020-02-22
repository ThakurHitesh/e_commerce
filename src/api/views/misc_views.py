from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .services import get_request_data, response, inv_serializer_error_response, error_response
from .base_views import BuyerBaseAPIView, BaseAPIView
from api.models.services import now
from api.services import generate_otp
from api.redis import save_otp_to_redis
from api.libraries import EmailGoogle
from api.constants import CONST_EMAIL_SEND_OTP_SUBJECT, CONST_EMAIL_SEND_OTP_MESSAGE, CONST_ERROR_MESSAGE_ADDRESS_COUNT_MAX_KEY, \
    CONST_ERROR_MESSAGE_INVALID_USER_KEY, CONST_ERROR_MESSAGE_PERMISSION_DENIED_KEY
from api.serializers import OTPSerializer, AddressSerializer, WishlistItemSerializer, WishlistSerializer
from api.permissions import IsBuyer
from api.models import Address, Wishlist, WishlistItem, Buyer

class SendOTPAPIView(APIView):
    """
    to send otp on mail to the user
    """
    serializer_class = OTPSerializer

    def post(self, request):
        request_data = get_request_data(request, 'post')
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid():
            otp = generate_otp()
            EmailGoogle.SendEmail(request_data["email"], CONST_EMAIL_SEND_OTP_SUBJECT, CONST_EMAIL_SEND_OTP_MESSAGE.format(otp=otp))
            save_otp_to_redis(request_data["email"], otp)
            return response({'OTP sent': True}, status.HTTP_200_OK)
        return inv_serializer_error_response(serializer, status.HTTP_400_BAD_REQUEST)

class AddressAPIView(BuyerBaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = AddressSerializer
    model = Address

    def post(self, request):
        request_data = get_request_data(request, 'post')
        request_data["buyer"] = request.user.id
        stored_address_count = self.model.get_active_objects(buyer_id=request.user.id).count()
        serializer = self.write_serializer_class(data=request_data)
        if stored_address_count < 3:
            if serializer.is_valid():
                obj = serializer.save()
                data = self.detail_serializer_class(obj).data
                return response(data, status.HTTP_201_CREATED)
            return inv_serializer_error_response(serializer, status.HTTP_400_BAD_REQUEST)
        return error_response(CONST_ERROR_MESSAGE_ADDRESS_COUNT_MAX_KEY, status.HTTP_406_NOT_ACCEPTABLE)

class WishlistAPIView(BuyerBaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = WishlistSerializer
    model = Wishlist

class WishlistItemAPIView(BaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = WishlistItemSerializer
    model = WishlistItem

    def post(self, request):
        request_data = get_request_data(request, 'post')
        wishlist_id = request_data["wishlist"] if request_data.get("wishlist") else None
        buyer = Buyer.get_active_objects(id=request.user.id)
        if buyer.exists():
            wishlist = Wishlist.get_active_objects(buyer_id=buyer[0].id)
            if str(wishlist_id) == str(wishlist[0].id): 
                serializer = self.write_serializer_class(data=request_data)
                if serializer.is_valid():
                    wishlistitem = serializer.save()
                    wishlist[0].update_total_items(True)
                    data = self.detail_serializer_class(wishlistitem).data
                    return response(data, status.HTTP_201_CREATED)
                return inv_serializer_error_response(serializer, status.HTTP_400_BAD_REQUEST)
            return error_response(CONST_ERROR_MESSAGE_PERMISSION_DENIED_KEY, status.HTTP_400_BAD_REQUEST)
        return error_response(CONST_ERROR_MESSAGE_INVALID_USER_KEY, status.HTTP_400_BAD_REQUEST)    
    
    def delete(self, request, pk):
        request_data = get_request_data(request, 'delete')
        queryset, serializer_class = self.get_queryset(pk)
        if queryset.exists():
            timestamp = now()
            instance = queryset[0]
            wishlist_id = instance.wishlist_id
            buyer = Buyer.get_active_objects(id=request.user.id)
            if buyer.exists():
                wishlist = Wishlist.get_active_objects(buyer_id=buyer[0].id)
                if str(wishlist_id) == str(wishlist[0].id):
                    instance.is_deleted = True
                    instance.deleted_at = timestamp
                    instance.modified_at = timestamp
                    instance.save()
                    wishlist[0].update_total_items(False)
                    return response({'deleted':True}, status.HTTP_200_OK)
                return error_response(CONST_ERROR_MESSAGE_PERMISSION_DENIED_KEY, status.HTTP_400_BAD_REQUEST)
            return error_response(CONST_ERROR_MESSAGE_INVALID_USER_KEY, status.HTTP_400_BAD_REQUEST)
        return error_response(CONST_ERROR_MESSAGE_INVALID_ID_KEY,status.HTTP_400_BAD_REQUEST)
