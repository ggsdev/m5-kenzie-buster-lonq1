from rest_framework import permissions
from rest_framework.views import Request


class IsResourceOwnerOrEmployeePermission(permissions.BasePermission):
    def has_object_permission(self, request: Request, view, user) -> bool:
        return request.user.is_employee or request.user.id == user.id
