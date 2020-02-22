import pytz
from django.utils import timezone
from django.conf import settings
import secrets, string

def now():
    return timezone.make_aware(timezone.datetime.now(), pytz.timezone(settings.TIME_ZONE))

def generate_random_checkout_order_id():
    """
    generate random checkout order id
    """
    prefix = "chk_"
    checkout_order_id = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for i in range(8))
    return  prefix+checkout_order_id