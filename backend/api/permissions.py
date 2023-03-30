from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс Permission, ограничивающий доступ к UnSAFE methods."""

    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_staff)


class IsReviewAndComment(permissions.BasePermission):
    """Класс Permission, ограничивающий доступ к рецептам."""

    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                or request.user.is_staff)

    def has_object_permission(self, request, view, obj):

        return (
            request.method not in permissions.SAFE_METHODS
            and (request.user.is_authenticated
                 and (request.user == obj.author
                      or request.user.is_staff))
            or request.method == ('GET')
        )
