from rest_framework.views import APIView
from rest_framework import status
from .services import get_request_data, get_paginated_params, paginated_response, inv_serializer_error_response, \
    response, error_response
from api.constants import CONST_ERROR_MESSAGE_INVALID_ID_KEY
from api.models.services import now

class BaseAPIView(APIView):
    """
    base api view for admin
    """

    def get_queryset(self, pk=None):
        if pk:
            queryset = self.model.get_active_objects().filter(id = pk)
            serializer_class = self.detail_serializer_class
        else:
            queryset = self.model.get_active_objects().all()
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

    def post(self, request):
        request_data = get_request_data(request, 'post')
        serializer = self.write_serializer_class(data=request_data)
        if serializer.is_valid():
            obj = serializer.save()
            data = self.detail_serializer_class(obj).data
            return response(data, status.HTTP_201_CREATED)
        return inv_serializer_error_response(serializer, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        request_data = get_request_data(request, 'put')
        queryset, serializer_class = self.get_queryset(pk)
        if queryset.exists():
            instance = queryset[0]
        serializer = self.update_serializer_class(instance=instance, data=request_data, partial=True)
        if serializer.is_valid():
            obj = serializer.save()
            data = serializer_class(obj).data
            return response(data, status.HTTP_200_OK)
        return inv_serializer_error_response(serializer, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        request_data = get_request_data(request, 'delete')
        queryset, serializer_class = self.get_queryset(pk)
        if queryset.exists():
            timestamp = now()
            instance = queryset[0]
            instance.is_deleted = True
            instance.deleted_at = timestamp
            instance.modified_at = timestamp
            instance.save()
            return response({'deleted':True}, status.HTTP_200_OK)
        return error_response(CONST_ERROR_MESSAGE_INVALID_ID_KEY,status.HTTP_400_BAD_REQUEST)

class SellerBaseAPIView(APIView):
    """
    base api view for seller
    """

    def get_queryset(self, pk=None):
        queryset = self.model.get_active_objects(seller_id=self.request.user.id if not self.request.user.is_anonymous else None)
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

    def post(self, request):
        request_data = get_request_data(request, 'post')
        request_data["seller"] = request.user.id
        serializer = self.write_serializer_class(data=request_data)
        if serializer.is_valid():
            obj = serializer.save()
            data = self.detail_serializer_class(obj).data
            return response(data, status.HTTP_201_CREATED)
        return inv_serializer_error_response(serializer, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        request_data = get_request_data(request, 'put')
        queryset, serializer_class = self.get_queryset(pk)
        if queryset.exists():
            instance = queryset[0]
        serializer = self.update_serializer_class(instance=instance, data=request_data, partial=True)
        if serializer.is_valid():
            obj = serializer.save()
            data = serializer_class(obj).data
            return response(data, status.HTTP_200_OK)
        return inv_serializer_error_response(serializer, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        request_data = get_request_data(request, 'delete')
        queryset, serializer_class = self.get_queryset(pk)
        if queryset.exists():
            timestamp = now()
            instance = queryset[0]
            instance.is_deleted = True
            instance.deleted_at = timestamp
            instance.modified_at = timestamp
            instance.save()
            return response({'deleted':True}, status.HTTP_200_OK)
        return error_response(CONST_ERROR_MESSAGE_INVALID_ID_KEY,status.HTTP_400_BAD_REQUEST)


class BuyerBaseAPIView(APIView):
    """
    base api view for buyer
    """

    def get_queryset(self, pk=None):
        queryset = self.model.get_active_objects(buyer_id=self.request.user.id if not self.request.user.is_anonymous else None)
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

    def post(self, request):
        request_data = get_request_data(request, 'post')
        request_data["buyer"] = request.user.id
        serializer = self.write_serializer_class(data=request_data)
        if serializer.is_valid():
            obj = serializer.save()
            data = self.detail_serializer_class(obj).data
            return response(data, status.HTTP_201_CREATED)
        return inv_serializer_error_response(serializer, status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        request_data = get_request_data(request, 'put')
        queryset, serializer_class = self.get_queryset(pk)
        if queryset.exists():
            instance = queryset[0]
        serializer = self.update_serializer_class(instance=instance, data=request_data, partial=True)
        if serializer.is_valid():
            obj = serializer.save()
            data = serializer_class(obj).data
            return response(data, status.HTTP_200_OK)
        return inv_serializer_error_response(serializer, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        request_data = get_request_data(request, 'delete')
        queryset, serializer_class = self.get_queryset(pk)
        if queryset.exists():
            timestamp = now()
            instance = queryset[0]
            instance.is_deleted = True
            instance.deleted_at = timestamp
            instance.modified_at = timestamp
            instance.save()
            return response({'deleted':True}, status.HTTP_200_OK)
        return error_response(CONST_ERROR_MESSAGE_INVALID_ID_KEY,status.HTTP_400_BAD_REQUEST)