from django.urls import path, include
from .user_urls import urlpatterns as user_urls
from .misc_urls import urlpatterns as misc_urls
from .product_urls import urlpatterns as product_urls
from .cart_urls import urlpatterns as cart_urls
from .payment_urls import urlpatterns as payment_urls

urlpatterns = [
    path('user/', include(user_urls)),
    path('misc/', include(misc_urls)),
    path('product/', include(product_urls)),
    path('cart/', include(cart_urls)),
    path('payment/', include(payment_urls)),
]
