from rest_framework import serializers
from api.models import Address, Wishlist, WishlistItem

class OTPSerializer(serializers.Serializer):
    """
    OTP serializer
    """
    email = serializers.EmailField()

class AddressSerializer(serializers.ModelSerializer):
    """
    Address serializer
    """
    class Meta:
        model = Address
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    """
    Wishlist serializer
    """
    class Meta:
        model = Wishlist
        fields = '__all__'
    
    def create(self, validate_data):
        wishlist = Wishlist.get_or_create_object(validate_data["buyer"].id)
        return wishlist

class WishlistItemSerializer(serializers.ModelSerializer):
    """
    WishlistItem serializer
    """
    class Meta:
        model = WishlistItem
        fields = '__all__'