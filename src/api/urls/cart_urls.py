from django.urls import path
from api.views import CartAPIView, CartItemAPIView, OrderAPIView, OrderForSellerAPIView

urlpatterns = [
    path('buyer-cart/', CartAPIView.as_view(), name='buyer-cart'),
    path('buyer-cart/<slug:pk>', CartAPIView.as_view(), name='buyer-cart'),
    path('buyer-cart-items/', CartItemAPIView.as_view(), name='buyer-cart-items'),
    path('buyer-cart-items/<slug:pk>', CartItemAPIView.as_view(), name='buyer-cart-items'),
    path('buyer-order/', OrderAPIView.as_view(), name='buyer-order'),
    path('buyer-order/<slug:pk>', OrderAPIView.as_view(), name='buyer-order'),
    path('seller-order/', OrderForSellerAPIView.as_view(), name='seller-order'),
    path('seller-order/<slug:pk>', OrderForSellerAPIView.as_view(), name='seller-order'),
]
