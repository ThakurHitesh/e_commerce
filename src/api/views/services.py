from django.conf import settings
from rest_framework.response import Response
from api.constants import CONST_ERROR_MESSAGE_TEMPLATES

def get_request_data(request, method_type):
    """
    return data within request
    """
    if method_type.lower()=='get':
        request_data = {}
        for key in request.GET:
            request_data[key] = request.GET[key]
    else:
        try:
            request_data = request.data
        except:
            request_data={}
    return request_data

def response(response, response_status):
    """
    return response with response status
    """
    if 200 <= response_status <= 207:
        response = {
            'success': True,
            'result': response,
        }
    return Response(response, response_status)

def error_response(template, response_status, template_data={}, error_code=1002):
    """
    return error response with user defineduser error template
    """
    error = {
        'error_code': error_code,
        'error_message': CONST_ERROR_MESSAGE_TEMPLATES[template].format(**template_data)
    }
    response = {
        'success': False,
        'error': error
    }
    return Response(response, response_status)

def inv_serializer_error_response(serializer, response_status, error_code=1003):
    """
    resturns error reponse on invalid serializer
    """
    error = {
        'error_code': error_code,
        'error_detail': serializer.errors
    }
    response = {
        'success': False,
        'error': error,
    }
    return Response(response, response_status)


def get_paginated_params(queryset, offset):
    page_size = settings.PAGE_SIZE
    start_index = offset*page_size
    try:
        count = queryset.count()
    except TypeError:
        count = len(queryset)
    except:
        queryset = [item for item in queryset]
        count = len(queryset)
    queryset = queryset[start_index: start_index+page_size]
    has_next = True if count > (offset+1)*page_size else False
    prev_page = min(0, offset-1) if offset > 1 else None
    next_page = offset+1 if has_next else None
    return (queryset, count, has_next, prev_page, next_page, offset)

def paginated_response(response, response_status, count, has_next, prev_page, next_page, offset):
    response = {
        'count': count,
        'has_next': has_next,
        'prev_page': prev_page,
        'next_page': next_page,
        'offset': offset,
        'result': response 
    }
    return Response(response, response_status)
