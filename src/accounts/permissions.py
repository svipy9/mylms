from rest_framework import permissions


class IsManagerUser(permissions.BasePermission):
    """
    Custom permission to only allow manager users to access the view.
    """

    def has_permission(self, request, _):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_manager
        )
