from rest_framework import serializers
from api.models import Cart, CartItem, Order, OrderForSeller

class CartSerializer(serializers.ModelSerializer):
    """
    Cart serializer
    """
    class Meta:
        model = Cart
        fields = '__all__'
    
    def create(self, validate_data):
        cart = Cart.get_or_create_object(validate_data["buyer"].id)
        return cart

class CartItemSerializer(serializers.ModelSerializer):
    """
    CartItem serializer
    """
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializer
    """
    class Meta:
        model = Order
        fields = '__all__'

class OrderForSellerSerializer(serializers.ModelSerializer):
    """
    OrderForSeller serializer
    """
    class Meta:
        model = OrderForSeller
        fields = '__all__'