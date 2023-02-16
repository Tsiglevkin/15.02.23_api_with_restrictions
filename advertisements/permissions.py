from rest_framework.permissions import BasePermission


class IsOwnerOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return request.creator.username == obj.creator.username
        # ошибка - нет атрибута creator. Также не находит атрибут ID.
