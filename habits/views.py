from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Habit
from .serializers import HabitSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class OwnHabitsOnlyPermission(permissions.BasePermission):
    """Разрешает пользователю видеть/редактировать только свои привычки."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = StandardResultsSetPagination
    # Важно: сначала глобальная защита (IsAuthenticated), потом кастомная
    permission_classes = [permissions.IsAuthenticated, OwnHabitsOnlyPermission]

    def get_queryset(self):
        # ГЛАВНАЯ ЗАЩИТА: если пользователь не авторизован, сразу возвращаем пустой список.
        # Это предотвращает ошибку TypeError при попытке сравнить AnonymousUser с ID.
        if not self.request.user.is_authenticated:
            return Habit.objects.none()

        # Если авторизован — фильтруем только его привычки
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
