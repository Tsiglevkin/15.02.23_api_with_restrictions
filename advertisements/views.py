from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadonly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['creator', 'status', 'created_at']
    search_fields = []  # требуется дозаполнить
    ordering_fields = []  # требуется дозаполнить

    permission_classes = [IsOwnerOrReadonly]  # требуется дозаполнить
    # authentication_classes = [TokenAuthentication]  # параметр обозначен в settings.py
    # pagination_class = PageNumberPagination  # параметр обозначен в settings.py

    def get_permissions(self):
        """Получение прав для действий."""  # Поправил заданный метод, для создания достаточно авторизации,
        # для правки - нужно быть владельцем

        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update"]:
            return [IsOwnerOrReadonly()]
        return []

    def perform_create(self, serializer):
        serializer.save(username=self.request.creator.username)


