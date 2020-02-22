from django.urls import path
from api.views import UserSignUpAPIView, UserLoginAPIView

urlpatterns = [
    path('register/', UserSignUpAPIView.as_view(), name="user-signup"),
    path('login/', UserLoginAPIView.as_view(), name="user-signin"),
]