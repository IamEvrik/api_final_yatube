"""Собственные классы разрешений."""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Редактировать публикацию может только её автор."""

    def has_object_permission(self, request, view, obj):
        """Ограничение доступа к объекту только для автора."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
        )
