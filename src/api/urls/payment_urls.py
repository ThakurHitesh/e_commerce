from django.urls import path
from api.views import PaymentAPIView

urlpatterns = [
    path('buyer-payment/', PaymentAPIView.as_view(), name='buyer-payment'),
]
