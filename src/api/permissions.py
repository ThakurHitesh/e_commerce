from rest_framework.permissions import BasePermission
from api.constants import CONST_CHOICE_USER_TYPE_BUYER, CONST_CHOICE_USER_TYPE_SELLER

class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_active and not request.user.is_deleted \
            and request.user.user_type == CONST_CHOICE_USER_TYPE_BUYER:
            return True
        return False

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_active and not request.user.is_deleted \
            and request.user.user_type == CONST_CHOICE_USER_TYPE_SELLER:
            return True
        return False

class IsBuyerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_active and not request.user.is_deleted \
            and (request.user.user_type == CONST_CHOICE_USER_TYPE_BUYER or request.user.is_staff):
            return True
        return False

class IsSellerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_active and not request.user.is_deleted \
            and (request.user.user_type == CONST_CHOICE_USER_TYPE_SELLER or request.user.is_staff):
            return True
        return False