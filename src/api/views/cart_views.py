from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from django.http import Http404
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .services import get_request_data, response, inv_serializer_error_response, error_response
from .base_views import BuyerBaseAPIView, BaseAPIView, SellerBaseAPIView
from api.models.services import now
from api.constants import CONST_ERROR_MESSAGE_INVALID_USER_KEY, CONST_ERROR_MESSAGE_PERMISSION_DENIED_KEY
from api.serializers import CartSerializer, CartItemSerializer, OrderSerializer, OrderForSellerSerializer
from api.permissions import IsBuyer, IsSeller
from api.models import Buyer, Cart, CartItem, Order, OrderForSeller

class CartAPIView(BuyerBaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = CartSerializer
    model = Cart

class CartItemAPIView(BaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = CartItemSerializer
    model = CartItem

    def post(self, request):
        request_data = get_request_data(request, 'post')
        cart_id = request_data["cart"] if request_data.get("cart") else None
        buyer = Buyer.get_active_objects(id=request.user.id)
        if buyer.exists():
            cart = Cart.get_active_objects(buyer_id=buyer[0].id)
            if str(cart_id) == str(cart[0].id): 
                serializer = self.write_serializer_class(data=request_data)
                if serializer.is_valid():
                    cartitem = serializer.save()
                    cart[0].update_total_items(True)
                    data = self.detail_serializer_class(cartitem).data
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
            cart_id = instance.cart_id
            buyer = Buyer.get_active_objects(id=request.user.id)
            if buyer.exists():
                cart = Cart.get_active_objects(buyer_id=buyer[0].id)
                if str(cart_id) == str(cart[0].id):
                    instance.is_deleted = True
                    instance.deleted_at = timestamp
                    instance.modified_at = timestamp
                    instance.save()
                    cart[0].update_total_items(False)
                    return response({'deleted':True}, status.HTTP_200_OK)
                return error_response(CONST_ERROR_MESSAGE_PERMISSION_DENIED_KEY, status.HTTP_400_BAD_REQUEST)
            return error_response(CONST_ERROR_MESSAGE_INVALID_USER_KEY, status.HTTP_400_BAD_REQUEST)
        return error_response(CONST_ERROR_MESSAGE_INVALID_ID_KEY,status.HTTP_400_BAD_REQUEST)

class OrderAPIView(BaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = OrderSerializer
    model = Order

    def post(self, request):
        request_data = get_request_data(request, 'post')
        cart_id = request_data["cart"] if request_data.get("cart") else None
        buyer = Buyer.get_active_objects(id=request.user.id)
        if buyer.exists():
            cart = Cart.get_active_objects(buyer_id=buyer[0].id)
            if str(cart_id) == str(cart[0].id): 
                serializer = self.write_serializer_class(data=request_data)
                if serializer.is_valid():
                    order = serializer.save()
                    data = self.detail_serializer_class(order).data
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
            cart_id = instance.cart_id
            buyer = Buyer.get_active_objects(id=request.user.id)
            if buyer.exists():
                cart = Cart.get_active_objects(buyer_id=buyer[0].id)
                if str(cart_id) == str(cart[0].id):
                    instance.is_deleted = True
                    instance.deleted_at = timestamp
                    instance.modified_at = timestamp
                    instance.save()
                    return response({'deleted':True}, status.HTTP_200_OK)
                return error_response(CONST_ERROR_MESSAGE_PERMISSION_DENIED_KEY, status.HTTP_400_BAD_REQUEST)
            return error_response(CONST_ERROR_MESSAGE_INVALID_USER_KEY, status.HTTP_400_BAD_REQUEST)
        return error_response(CONST_ERROR_MESSAGE_INVALID_ID_KEY,status.HTTP_400_BAD_REQUEST)

class OrderForSellerAPIView(SellerBaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSeller)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = OrderForSellerSerializer
    model = OrderForSeller

    def post(self, request):
        raise Http404

    def delete(self, post, pk):
        raise Http404