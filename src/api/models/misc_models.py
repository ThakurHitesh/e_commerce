from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .services import now
from api.models import TimeStamp, Buyer, Product
from api.constants import CONST_USER_ADDRESS_LENGTH, CONS_USER_ADDRESS_HOUSE_NAME_LENGTH, CONS_USER_ADDRESS_LANDMARK_LENGTH, \
    CONST_CHOICE_USER_ADDRESS_TYPE_HOME, CONST_CHOICES_USER_ADDRESS_TYPE, CONST_USER_ADDRESS_TYPE_LENGTH

class Address(TimeStamp):
    """
    model contains user's address 
    """
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    address = models.TextField(max_length=CONST_USER_ADDRESS_LENGTH)
    house_name = models.CharField(max_length=CONS_USER_ADDRESS_HOUSE_NAME_LENGTH, null=True, blank=True)
    house_no = models.IntegerField(null=True, blank=True)
    landmark = models.CharField(max_length=CONS_USER_ADDRESS_LANDMARK_LENGTH, null=True, blank=True)
    pincode = models.IntegerField()
    address_type = models.CharField(choices=CONST_CHOICES_USER_ADDRESS_TYPE, default=CONST_CHOICE_USER_ADDRESS_TYPE_HOME, max_length=CONST_USER_ADDRESS_TYPE_LENGTH)

class Wishlist(TimeStamp):
    """
    wishlist model for buyer
    """
    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE)
    total_items = models.PositiveIntegerField(default=0)

    @classmethod
    def get_or_create_object(cls, buyer_id):
        obj = cls.get_active_objects(buyer_id=buyer_id)
        if obj.exists():
            return obj[0]
        obj = cls.objects.create(buyer_id=buyer_id)
        return obj
    
    def update_total_items(self, flag):
        if not flag and self.total_items > 0:
            self.total_items -= 1
        if flag:
            self.total_items += 1
        self.save()

class WishlistItem(TimeStamp):
    """
    model contains product in a wishlist
    """
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('wishlist', 'product',)

    def __str__(self):
        return "{}".format(self.product.name)


@receiver(post_delete, sender=WishlistItem)
def update_wishlist_total_items(sender, instance, **kwargs):
    wishlist_id = instance.wishlist
    wishlist_obj = Wishlist.get_active_objects(id=str(wishlist_id))[0]
    wishlist_obj.update_total_items(False)