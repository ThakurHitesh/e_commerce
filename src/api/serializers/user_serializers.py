from rest_framework import serializers
from django.core.validators import MinLengthValidator, MaxLengthValidator
from api.models import User, Buyer, Seller, Admin
from api.services import generate_random_password, generate_random_username
from api.constants import CONST_CHOICE_USER_TYPE_BUYER, CONST_CHOICE_USER_TYPE_SELLER, CONST_CHOICE_USER_TYPE_ADMIN, \
    CONST_USER_TYPE_LENGTH

class UserSignUpSerializer(serializers.ModelSerializer):
    """
    serializer for user sign up
    """
    otp = serializers.CharField(validators=[MinLengthValidator(4), MaxLengthValidator(4)])

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'country_code', 'contact_no', 'user_type', 'otp']
    
    def create(self, validated_data):
        validated_data.pop("otp")
        password = generate_random_password()
        validated_data["username"] = generate_random_username()
        validated_data["name"] = validated_data["first_name"]+" "+validated_data["last_name"]
        user = User(**validated_data)
        user.set_password(password)
        if validated_data["user_type"].lower()==CONST_CHOICE_USER_TYPE_ADMIN:
            user.is_staff = True
        user.save()
        if validated_data["user_type"].lower()==CONST_CHOICE_USER_TYPE_BUYER:
            return Buyer.objects.create(user=user)
        if validated_data["user_type"].lower()==CONST_CHOICE_USER_TYPE_SELLER:
            return Seller.objects.create(user=user)
        if validated_data["user_type"].lower()==CONST_CHOICE_USER_TYPE_ADMIN:
            return Admin.objects.create(user=user)

class BuyerSerializer(serializers.ModelSerializer):
    """
    serializer for buyer
    """
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField()
    contact_no = serializers.SerializerMethodField()
    image =  serializers.SerializerMethodField()

    class Meta:
        model = Buyer
        fields = '__all__'

    def get_name(self, instance):
        return User.objects.filter(id=instance.id)[0].name
    
    def get_email(self, instance):
        return User.objects.filter(id=instance.id)[0].email
    
    def get_country_code(self, instance):
        return User.objects.filter(id=instance.id)[0].country_code

    def get_contact_no(self, instance):
        return User.objects.filter(id=instance.id)[0].contact_no
    
    def get_image(self, instance):
        return User.objects.filter(id=instance.id)[0].image.name

class SellerSerializer(serializers.ModelSerializer):
    """
    serializer for seller
    """
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField()
    contact_no = serializers.SerializerMethodField()
    image =  serializers.SerializerMethodField()
    
    class Meta:
        model = Seller
        fields = '__all__'
    
    def get_name(self, instance):
        return User.objects.filter(id=instance.id)[0].name
    
    def get_email(self, instance):
        return User.objects.filter(id=instance.id)[0].email
    
    def get_country_code(self, instance):
        return User.objects.filter(id=instance.id)[0].country_code

    def get_contact_no(self, instance):
        return User.objects.filter(id=instance.id)[0].contact_no
    
    def get_image(self, instance):
        return User.objects.filter(id=instance.id)[0].image.name

class AdminSerializer(serializers.ModelSerializer):
    """
    serializer for Admin
    """
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    country_code = serializers.SerializerMethodField()
    contact_no = serializers.SerializerMethodField()
    image =  serializers.SerializerMethodField()
    
    class Meta:
        model = Admin
        fields = '__all__'
    
    def get_name(self, instance):
        return User.objects.filter(id=instance.id)[0].name
    
    def get_email(self, instance):
        return User.objects.filter(id=instance.id)[0].email
    
    def get_country_code(self, instance):
        return User.objects.filter(id=instance.id)[0].country_code

    def get_contact_no(self, instance):
        return User.objects.filter(id=instance.id)[0].contact_no
    
    def get_image(self, instance):
        return User.objects.filter(id=instance.id)[0].image.name

class UserReadSerializer(serializers.Serializer):
    """
    return serializer on the basis of instance
    """
    def to_representation(self, instance):
        if isinstance(instance, Buyer):
            return BuyerSerializer(instance, context=self.context).data
        if isinstance(instance, Seller):
            return SellerSerializer(instance, context=self.context).data 
        if isinstance(instance, Admin):
            return AdminSerializer(instance, context=self.context).data 

class UserLoginSerializer(serializers.Serializer):
    """
    User Login Serializer
    """
    email = serializers.EmailField()
    otp = serializers.CharField(validators=[MinLengthValidator(4), MaxLengthValidator(4)])
    user_typr = serializers.CharField(max_length=CONST_USER_TYPE_LENGTH)
