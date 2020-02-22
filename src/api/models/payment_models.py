from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from api.models import TimeStamp, Order
from api.constants import CONST_LENGTH_PAYMENT_RAZORPAY_ID, CONST_CHOICES_LENGTH_PAYMENT_CURRENCY, CONST_NAME_LENGTH, \
    CONST_CHOICES_PAYMENT_CURRENCY, CONST_CHOICE_PAYMENT_CURRENCY_INR

razorpay_client = getattr(settings, 'RAZORPAY_CONNECTION')

class Payment(TimeStamp):
    """
    Order payment
    """
    cart_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=CONST_LENGTH_PAYMENT_RAZORPAY_ID, null=True, blank=True)
    amount = models.PositiveIntegerField()
    currency = models.CharField(choices=CONST_CHOICES_PAYMENT_CURRENCY,
         max_length=CONST_CHOICES_LENGTH_PAYMENT_CURRENCY, default=CONST_CHOICE_PAYMENT_CURRENCY_INR)
    status = models.CharField(max_length=CONST_NAME_LENGTH, null=True, blank=True)
    order_id = models.CharField(max_length=CONST_LENGTH_PAYMENT_RAZORPAY_ID, null=True, blank=True)
    method = models.CharField(max_length=CONST_NAME_LENGTH, null=True, blank=True)
    card_id = models.CharField(max_length=CONST_LENGTH_PAYMENT_RAZORPAY_ID, null=True, blank=True)
    cname = models.CharField(max_length=CONST_NAME_LENGTH, null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    cnetwork = models.CharField(max_length=CONST_NAME_LENGTH, null=True, blank=True)
    ctype = models.CharField(max_length=CONST_NAME_LENGTH, null=True, blank=True)
    bank = models.CharField(max_length=CONST_NAME_LENGTH, null=True, blank=True)
    wallet = models.CharField(max_length=CONST_NAME_LENGTH, null=True, blank=True)
    vpa =  models.CharField(max_length=CONST_NAME_LENGTH, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contact = models.BigIntegerField(null=True, blank=True)
    notes = JSONField(blank=True, null=True)
    attempts = models.PositiveIntegerField(default=0)

    @classmethod
    def create_payment(cls, cart_order, amount, currency, status):
        """
        It creates an order for a payment
        """
        cart_order_id = cart_order.id
        amount = amount*100
        
        data = {
            "amount": amount,
            "currency": currency,
            "payment_capture": 1
        }
        order_response = razorpay_client.order.create(data=data)
        obj = cls.objects.create(
            cart_order_id=cart_order_id,
            amount=order_response['amount'],
            order_id=order_response['id'],
            currency=order_response['currency'],
            attempts=order_response['attempts'],
            status=status
        )
        return obj


    @classmethod
    def update_payment_from_webhook(cls, payload):
        """
        Updates payment from razorpay Webhook
        """
        try:
            webhook_response = payload['payment']['entity']
            obj = cls.get_active_objects(order_id=webhook_response['order_id'])
            if obj.exists():
                if webhook_response['method'] == 'card':
                    obj.update(
                        payment_id=webhook_response['id'],
                        method=webhook_response['method'],
                        card_id=webhook_response['card_id'],
                        cname=webhook_response['card']['name'],
                        last4 = webhook_response['card']['last4'],
                        cnetwork = webhook_response['card']['network'],
                        ctype = webhook_response['card']['type'],
                        bank = webhook_response['bank'],
                        wallet = webhook_response['wallet'],
                        vpa = webhook_response['vpa'],
                        email = webhook_response['email'],
                        contact = webhook_response['contact'],
                        notes = webhook_response['notes']
                    )
                else:
                    obj.update(
                        payment_id=webhook_response['id'],
                        method=webhook_response['method'],
                        card_id=webhook_response['card_id'],
                        bank=webhook_response['bank'],
                        wallet=webhook_response['wallet'],
                        vpa=webhook_response['vpa'],
                        email=webhook_response['email'],
                        contact=webhook_response['contact'],
                        notes=webhook_response['notes']
                    )
                obj = obj[0]
                if webhook_response['status'] == CONST_PAYMENT_STATUS_CAPTURED:
                    obj.status = CONST_PAYMENT_STATUS_CAPTURED
                    obj.save()
                elif webhook_response['status'] == CONST_PAYMENT_STATUS_AUTHORIZED and (obj.status == CONST_PAYMENT_STATUS_CREATED
                                                                                        or obj.status == CONST_PAYMENT_STATUS_FAILED):
                    obj.status = CONST_PAYMENT_STATUS_AUTHORIZED
                    obj.save()
                elif webhook_response['status'] == CONST_PAYMENT_STATUS_FAILED and (obj.status == CONST_PAYMENT_STATUS_CREATED
                                                                                    or obj.status == CONST_PAYMENT_STATUS_AUTHORIZED):
                    obj.status = CONST_PAYMENT_STATUS_FAILED
                    obj.save()
        except Exception as err:
            send_error_report_email(str(traceback.format_exc()), inspect.stack()[0][3])
