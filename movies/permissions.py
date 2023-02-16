from rest_framework import permissions
from rest_framework.views import Request, View


class IsResourceOwnerOrEmployeePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.user.is_authenticated
            and request.user.is_employee
            or request.user.id == request.query_params.user_id
        )


class IsEmployeePermission(permissions.BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_employee
        )
