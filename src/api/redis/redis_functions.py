from django.conf import settings
from .redis_keys import TTL_SENT_OTP

REDIS_CONNECTION = getattr(settings, 'REDIS_CONNECTION')

def save_otp_to_redis(email, otp):
    print(REDIS_CONNECTION)
    REDIS_CONNECTION.set(email, otp)
    REDIS_CONNECTION.expire(email, TTL_SENT_OTP)

def verify_otp(email, otp):
    save_otp = REDIS_CONNECTION.get(email)
    if otp is not None: 
        if save_otp.decode('utf-8') == otp:
            return True
    return False 