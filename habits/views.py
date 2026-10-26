from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError  # <-- Один импорт вверху, этого достаточно
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
    permission_classes = [permissions.IsAuthenticated, OwnHabitsOnlyPermission]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Habit.objects.none()
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        data = serializer.validated_data

        # Проверка reward: строка не пустая и не только пробелы
        has_reward = bool(data.get('reward') and str(data.get('reward')).strip())

        # Проверка related_habit: просто наличие объекта (DRF уже превратил ID в объект)
        related_habit_obj = data.get('related_habit')
        has_related = related_habit_obj is not None

        is_pleasant = data.get('is_pleasant', False)

        # 1. Конфликт: reward и related_habit одновременно
        if has_reward and has_related:
            raise ValidationError({
                "non_field_errors": [
                    "Нельзя указать и вознаграждение, и связанную привычку одновременно."
                ]
            })

        # 2. Проверка для приятной привычки
        if is_pleasant:
            if has_reward:
                raise ValidationError({"reward": ["Приятная привычка не может иметь вознаграждение."]})

            if has_related:
                raise ValidationError({"related_habit": ["Приятная привычка не может иметь связанную привычку."]})

        serializer.save(user=self.request.user)
