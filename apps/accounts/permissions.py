from rest_framework import permissions


class IsTelegramUser(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'sizda telegram ulanmagan'

    def has_permission(self, request, view):
        return request.user and request.user.telegram_id