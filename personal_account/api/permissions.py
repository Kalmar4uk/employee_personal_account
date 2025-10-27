from django.conf import settings
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class BotOrStandartPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        token = request.headers.get("token")
        if (
            request.user.is_authenticated
            or (
                (token := request.headers.get("token"))
                and token == settings.SECRET_KEY_FOR_REQUEST
            )
        ):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.headers.get("token"):
            raise PermissionDenied("Permission denied")
        return True
