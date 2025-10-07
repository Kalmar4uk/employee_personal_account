from django.conf import settings
from rest_framework import permissions


class ForBotRequestPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if (
            (token := request.headers.get("token"))
            and token == settings.SECRET_KEY_FOR_REQUEST
        ):
            return True
        return False


class PostRequestForTokenOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method == "POST"
