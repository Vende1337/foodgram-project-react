from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс Permission, ограничивающий доступ к UnSAFE methods."""

    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_staff)


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        return ((request.method == ('GET') or ('POST')) 
                or request.user.is_authenticated
                and request.user.is_staff)

