from django.urls import path, include
from .base_urls import urlpatterns as base_urls

urlpatterns = [
    path('', include(base_urls)),
]
