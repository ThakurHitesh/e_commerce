from django.urls import path
from api.views import SendOTPAPIView, AddressAPIView, WishlistAPIView,WishlistItemAPIView

urlpatterns = [
    path('send-otp/', SendOTPAPIView.as_view(), name="user-send-otp"),
    path('buyer-address/', AddressAPIView.as_view(), name="buyer-address"),
    path('buyer-address/<slug:pk>/', AddressAPIView.as_view(), name="buyer-address"),
    path('buyer-wishlist/', WishlistAPIView.as_view(), name="buyer-wishlist"),
    path('buyer-wishlist/<slug:pk>/', WishlistAPIView.as_view(), name="buyer-wishlist"),
    path('buyer-wishlist-items/', WishlistItemAPIView.as_view(), name="buyer-wishlist-itmes"),
    path('buyer-wishlist-items/<slug:pk>/', WishlistItemAPIView.as_view(), name="buyer-wishlist-items"),
]