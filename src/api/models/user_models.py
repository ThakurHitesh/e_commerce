from django.db import models
from django.core.validators import MinValueValidator
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import AbstractUser
from api.models import TimeStamp, BaseNameModel, BaseUniqueNameModel
from api.constants import CONST_NAME_LENGTH, CONST_CHOICES_USER_TYPE, CONST_USER_TYPE_LENGTH, CONST_EMAIL_LENGTH


class User(AbstractUser, TimeStamp):
    """
    model containing user fields
    """
    name = models.CharField(max_length=CONST_NAME_LENGTH, null=True, blank=True)
    email = models.EmailField(max_length=CONST_EMAIL_LENGTH, verbose_name='email address')
    country_code = models.PositiveIntegerField()
    contact_no = models.BigIntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='profile_images', blank=True, null=True, default='profile_default_image.jpg')
    user_type = models.CharField(choices=CONST_CHOICES_USER_TYPE, max_length=CONST_USER_TYPE_LENGTH)

    class Meta:
        unique_together = ('email', 'user_type',)

    def __str__(self):
        return "{}".format(self.name)

    def create_auth_token(self):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self)
        payload["user_type"] = self.user_type
        payload["email"] = self.email
        token = jwt_encode_handler(payload)
        return 'JWT '+token

class Buyer(TimeStamp):
    """
    model containing buyer fields
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.id = self.user.id
        return super(Buyer, self).save(*args, **kwargs)
    

class Seller(TimeStamp):
    """
    model containing seller fields
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.id = self.user.id
        return super(Seller, self).save(*args, **kwargs)

class Admin(TimeStamp):
    """
    model containing Addmin fields
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.id = self.user.id
        return super(Admin, self).save(*args, **kwargs)
