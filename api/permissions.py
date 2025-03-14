from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'admin'



class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'owner'

