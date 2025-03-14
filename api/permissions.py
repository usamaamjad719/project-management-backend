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



class IsProjectOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only project owners to edit or delete.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the project
        return obj.created_by == request.user

class IsProjectRoleOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only project role owners to edit or delete.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only comment owners to edit or delete.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
