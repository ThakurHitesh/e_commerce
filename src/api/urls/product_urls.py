from django.urls import path
from api.views import CategoryAPIView, GetProductCategoryAPIView, ProductAPIView, GetProductAPIView, \
    ProductQuestionsAPIView, GetProductQuestionsAPIView, ProductAnswersAPIView, GetProductAnswersAPIView, \
    ReviewsAPIView, GetReviewsAPIView, ProductImagesAPIView, GetProductImagesAPIView

urlpatterns = [
    path('admin-category/', CategoryAPIView.as_view(), name='admin-category'),
    path('admin-category/<slug:pk>/', CategoryAPIView.as_view(), name='admin-category'),
    path('seller-product/', ProductAPIView.as_view(), name='seller-product'),
    path('seller-product/<slug:pk>/', ProductAPIView.as_view(), name='seller-product'),
    path('seller-product-images/', ProductImagesAPIView.as_view(), name='seller-product-images'),
    path('seller-product-images/<slug:pk>/', ProductImagesAPIView.as_view(), name='seller-product-images'),
    path('buyer-product-question/', ProductQuestionsAPIView.as_view(), name='buyer-product-question'),
    path('buyer-product-question/<slug:pk>/', ProductQuestionsAPIView.as_view(), name='buyer-product-question'),
    path('buyer-product-answer/', ProductAnswersAPIView.as_view(), name='buyer-product-answer'),
    path('buyer-product-answer/<slug:pk>/', ProductAnswersAPIView.as_view(), name='buyer-product-answer'),
    path('buyer-product-review/', ReviewsAPIView.as_view(), name='buyer-product-review'),
    path('buyer-product-review/<slug:pk>/', ReviewsAPIView.as_view(), name='buyer-product-review'),
    path('product-category/', GetProductCategoryAPIView.as_view(), name='product-category'),
    path('product-category/<slug:pk>/', GetProductCategoryAPIView.as_view(), name='product-category'),
    path('product/', GetProductAPIView.as_view(), name='product'),
    path('product/<slug:pk>/', GetProductAPIView.as_view(), name='product'),
    path('product-question/', GetProductQuestionsAPIView.as_view(), name='product-question'),
    path('product-question/<slug:pk>/', GetProductQuestionsAPIView.as_view(), name='product-question'),
    path('product-answer/', GetProductAnswersAPIView.as_view(), name='product-answer'),
    path('product-answer/<slug:pk>/', GetProductAnswersAPIView.as_view(), name='product-answer'),
    path('product-review/', GetReviewsAPIView.as_view(), name='product-review'),
    path('product-review/<slug:pk>/', GetReviewsAPIView.as_view(), name='product-review'),
    path('product-images/', GetProductImagesAPIView.as_view(), name='product-images'),
    path('product-images/<slug:pk>/', GetProductImagesAPIView.as_view(), name='product-images'),
]
