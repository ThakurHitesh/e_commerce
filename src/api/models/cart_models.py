from .services import now, generate_random_checkout_order_id
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.db import models
from django.contrib.postgres.fields import JSONField
from api.models import TimeStamp, Buyer, Product, Address, Seller
from api.constants import CONST_CHECKOUT_ORDER_ID_LENGTH, CONST_CHOICES_ORDER_STATUS, \
    CONST_CHOICE_ORDER_STATUS_PLACED, CONST_CHOICE_ORDER_STATUS_LENGTH, CONST_PRODUCT_ORDER_ID_LENGTH

class Cart(TimeStamp):
    """
    Cart model
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

class CartItem(TimeStamp):
    """
    model contains cart items
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    gift_wrap = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.product.name)

class Order(TimeStamp):
    """
    user order model
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    checkout_order_id = models.CharField(max_length=CONST_CHECKOUT_ORDER_ID_LENGTH, default=generate_random_checkout_order_id)
    shipping_address = JSONField()
    total_amount = models.PositiveIntegerField()
    order_created_at = models.DateTimeField(default=now) 
    order_status = models.CharField(choices=CONST_CHOICES_ORDER_STATUS, default=CONST_CHOICE_ORDER_STATUS_PLACED, max_length=CONST_CHOICE_ORDER_STATUS_LENGTH)


class OrderForSeller(TimeStamp):
    """
    orders placed and to be delivered
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    gift_wrap = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_address = JSONField()
    amount = models.PositiveIntegerField()
    has_delivered = models.BooleanField(default=False)

    class Meta:
        unique_together = ('product', 'order',)

    def __str__(self):
        return "{}".format(self.product.name)

@receiver(post_delete, sender=CartItem)
def update_cart_total_items(sender, instance, **kwargs):
    cart_id = instance.cart
    cart_obj = Cart.get_active_objects(id=str(cart_id))[0]
    cart_obj.update_total_items(False)

@receiver(post_save, sender=Order)
def update_order_for_seller(sender, instance, **kwargs):
    queryset = CartItem.get_active_objects(cart_id=instance.cart)
    for item in queryset:
        price = item.product.base_price if item.product.seller_price is None else item.product.seller_price
        final_price = price - (price*item.product.discount)/100
        OrderForSeller.objects.create(
            product_id = item.product_id,
            seller_id = item.product.seller_id,
            quantity = item.quantity,
            gift_wrap = item.gift_wrap,
            order_id = instance.id,
            shipping_address = instance.shipping_address,
            amount = final_price
            )
