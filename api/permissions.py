from rest_framework import permissions


class IsMemberPermission(permissions.BasePermissionMetaclass):
    def get_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return bool(request.user and (request.user.is_administrator or request.user.is_moder))