from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions
from rest_framework import status
from django.http import Http404
from api.views import BaseAPIView, SellerBaseAPIView, BuyerBaseAPIView
from api.models import Category, Product, ProductQuestions, ProductAnswers, Reviews, ProductImages
from api.serializers import CategorySerializer, ProductSerializer, ProductQuestionsSerializer, ProductAnswersSerializer, \
    ReviewsSerializer, ProductImagesSerializer
from api.permissions import IsSeller, IsBuyer, IsBuyerOrAdmin, IsSellerOrAdmin
from .services import get_request_data, get_paginated_params, paginated_response, response, error_response, inv_serializer_error_response


class CategoryAPIView(BaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = CategorySerializer
    model = Category


class GetProductCategoryAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    read_serializer_class = detail_serializer_class = CategorySerializer
    model = Category

    def get_queryset(self, pk=None):
        queryset = self.model.get_active_objects()
        if pk:
            queryset = queryset.filter(id = pk)
            serializer_class = self.detail_serializer_class
        else:
            serializer_class = self.read_serializer_class
        return queryset, serializer_class

    def get(self, request, pk=None):
        request_data = get_request_data(request, 'get')
        offset = int(request_data.pop("offset", 0))
        queryset, serializer_class = self.get_queryset(pk)
        if pk:
            data = serializer_class(queryset, many=True).data
            return response(data, status.HTTP_200_OK)    
        queryset, count, has_next, prev_page, next_page, offset = get_paginated_params(queryset, offset)
        data = serializer_class(queryset, many=True).data
        return paginated_response(data, status.HTTP_200_OK, count, has_next, prev_page, next_page, offset)


class ProductAPIView(SellerBaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSeller)
    
    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = ProductSerializer
    model = Product
    

class GetProductAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyerOrAdmin)
    
    read_serializer_class = detail_serializer_class = ProductSerializer
    model = Product

    def get_queryset(self, pk=None):
        queryset = self.model.get_active_objects()
        if pk:
            queryset = queryset.filter(id = pk)
            serializer_class = self.detail_serializer_class
        else:
            serializer_class = self.read_serializer_class
        return queryset, serializer_class

    def get(self, request, pk=None):
        request_data = get_request_data(request, 'get')
        offset = int(request_data.pop("offset", 0))
        queryset, serializer_class = self.get_queryset(pk)
        if pk:
            data = serializer_class(queryset, many=True).data
            return response(data, status.HTTP_200_OK)    
        if request_data.get('categories'):
            queryset = queryset.filter(categories=request_data['categories'])
        queryset, count, has_next, prev_page, next_page, offset = get_paginated_params(queryset, offset)
        data = serializer_class(queryset, many=True).data
        return paginated_response(data, status.HTTP_200_OK, count, has_next, prev_page, next_page, offset)


class ProductImagesAPIView(BaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSeller)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = ProductImagesSerializer
    model = ProductImages

    def get(self, request, pk=None):
        raise Http404

class GetProductImagesAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    read_serializer_class = detail_serializer_class = ProductImagesSerializer
    model = ProductImages

    def get_queryset(self, pk=None):
        queryset = self.model.get_active_objects()
        if pk:
            queryset = queryset.filter(id = pk)
            serializer_class = self.detail_serializer_class
        else:
            serializer_class = self.read_serializer_class
        return queryset, serializer_class

    def get(self, request, pk=None):
        request_data = get_request_data(request, 'get')
        offset = int(request_data.pop("offset", 0))
        queryset, serializer_class = self.get_queryset(pk)
        if pk:
            data = serializer_class(queryset, many=True).data
            return response(data, status.HTTP_200_OK)    
        if request_data.get('product'):
            queryset = queryset.filter(product_id=request_data['product'])
        queryset, count, has_next, prev_page, next_page, offset = get_paginated_params(queryset, offset)
        data = serializer_class(queryset, many=True).data
        return paginated_response(data, status.HTTP_200_OK, count, has_next, prev_page, next_page, offset)


class ProductQuestionsAPIView(BuyerBaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = ProductQuestionsSerializer
    model = ProductQuestions

    def get(self, request, pk=None):
        raise Http404


class GetProductQuestionsAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    read_serializer_class = detail_serializer_class = ProductQuestionsSerializer
    model = ProductQuestions

    def get_queryset(self, pk=None):
        queryset = self.model.get_active_objects()
        if pk:
            queryset = queryset.filter(id = pk)
            serializer_class = self.detail_serializer_class
        else:
            serializer_class = self.read_serializer_class
        return queryset, serializer_class

    def get(self, request, pk=None):
        request_data = get_request_data(request, 'get')
        offset = int(request_data.pop("offset", 0))
        queryset, serializer_class = self.get_queryset(pk)
        if pk:
            data = serializer_class(queryset, many=True).data
            return response(data, status.HTTP_200_OK)    
        if request_data.get('product'):
            queryset = queryset.filter(product_id=request_data['product'])
        queryset, count, has_next, prev_page, next_page, offset = get_paginated_params(queryset, offset)
        data = serializer_class(queryset, many=True).data
        return paginated_response(data, status.HTTP_200_OK, count, has_next, prev_page, next_page, offset)


class ProductAnswersAPIView(BuyerBaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = ProductAnswersSerializer
    model = ProductAnswers

    def get(self, request, pk=None):
        raise Http404


class GetProductAnswersAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    read_serializer_class = detail_serializer_class = ProductAnswersSerializer
    model = ProductAnswers

    def get_queryset(self, pk=None):
        queryset = self.model.get_active_objects()
        if pk:
            queryset = queryset.filter(id = pk)
            serializer_class = self.detail_serializer_class
        else:
            serializer_class = self.read_serializer_class
        return queryset, serializer_class

    def get(self, request, pk=None):
        request_data = get_request_data(request, 'get')
        offset = int(request_data.pop("offset", 0))
        queryset, serializer_class = self.get_queryset(pk)
        if pk:
            data = serializer_class(queryset, many=True).data
            return response(data, status.HTTP_200_OK)    
        if request_data.get('question'):
            queryset = queryset.filter(question_id=request_data['question'])
        queryset, count, has_next, prev_page, next_page, offset = get_paginated_params(queryset, offset)
        data = serializer_class(queryset, many=True).data
        return paginated_response(data, status.HTTP_200_OK, count, has_next, prev_page, next_page, offset)

class ReviewsAPIView(BuyerBaseAPIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)

    read_serializer_class = detail_serializer_class = update_serializer_class = write_serializer_class = ReviewsSerializer
    model = Reviews

    def get(self, request, pk=None):
        raise Http404


class GetReviewsAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    read_serializer_class = detail_serializer_class = ReviewsSerializer
    model = Reviews

    def get_queryset(self, pk=None):
        queryset = self.model.get_active_objects()
        if pk:
            queryset = queryset.filter(id = pk)
            serializer_class = self.detail_serializer_class
        else:
            serializer_class = self.read_serializer_class
        return queryset, serializer_class

    def get(self, request, pk=None):
        request_data = get_request_data(request, 'get')
        offset = int(request_data.pop("offset", 0))
        queryset, serializer_class = self.get_queryset(pk)
        if pk:
            data = serializer_class(queryset, many=True).data
            return response(data, status.HTTP_200_OK)    
        if request_data.get('product'):
            queryset = queryset.filter(product_id=request_data['product'])
        queryset, count, has_next, prev_page, next_page, offset = get_paginated_params(queryset, offset)
        data = serializer_class(queryset, many=True).data
        return paginated_response(data, status.HTTP_200_OK, count, has_next, prev_page, next_page, offset)
