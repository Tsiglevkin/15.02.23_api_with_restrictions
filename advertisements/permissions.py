from rest_framework.permissions import BasePermission


class IsOwnerOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        pass
