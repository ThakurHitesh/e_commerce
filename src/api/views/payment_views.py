from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .services import get_request_data, response, inv_serializer_error_response, error_response
from api.permissions import IsBuyer
from api.serializers import PaymentSerializer
from api.models import Payment

class PaymentAPIView(APIView):
    """
    Payment views
    """
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, IsBuyer]
    serializer_class = PaymentSerializer
    model = Payment

    def post(self, request):
        request_data = get_request_data(request, 'post')
        serializer = self.serializer_class(data=request_data)
        if serializer.is_valid():
            data = serializer.save()
            return response(data, status.HTTP_201_CREATED)
        return inv_serializer_error_response(serializer, status.HTTP_400_BAD_REQUEST)
