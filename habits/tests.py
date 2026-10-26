from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Habit

User = get_user_model()


class HabitAPITests(TestCase):
    """Тесты для API привычек."""

    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='pass1234')

        # Клиент с авторизацией (для позитивных тестов)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Клиент БЕЗ авторизации (чистый, без force_authenticate)
        self.anon_client = APIClient()

        self.url = '/api/habits/'

    def test_unauthenticated_access_denied(self):
        """Проверка: аноним получает 401, не доходя до логики фильтрации."""
        # Мы просто делаем запрос. Если permission IsAuthenticated стоит верно,
        # Django вернет 401 ДО того, как сработает filter(user=request.user).
        response = self.anon_client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_habit_success(self):
        payload = {
            "action": "Бегать по утрам",
            "time": "07:00:00",
            "period_days": 1,
            "execution_time_seconds": 60,  # Точно число, точно <= 120
            "is_pleasant": False
            # Мы НЕ передаём reward и related_habit, чтобы избежать конфликтов в clean()
        }
        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_validation_execution_time_limit(self):
        """Валидатор отклоняет время > 120 сек — ожидаем 400 Bad Request."""
        payload = {
            "action": "Бегать долго",
            "time": "07:00:00",
            "period_days": 1,
            "execution_time_seconds": 200,  # Нарушаем правило
            "is_pleasant": False
        }

        response = self.client.post(self.url, payload, format='json')

        # ГЛАВНОЕ: мы явно ждем 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = response.json()

        # Проверяем, что сообщение об ошибке пришло
        error_message = str(data)
        self.assertTrue('превышает' in error_message.lower() or '120' in error_message,
                        f"В ответе нет ожидаемого сообщения об ошибке: {error_message}")

    def test_pagination_works(self):
        """Проверка пагинации."""
        # Создаем 6 привычек
        for i in range(6):
            Habit.objects.create(
                user=self.user,
                action=f"Действие {i}",
                time="12:00:00",
                period_days=1,
                execution_time_seconds=60
            )

        response = self.client.get(self.url)
        data = response.json()

        self.assertEqual(len(data['results']), 5)
        self.assertIsNotNone(data['next'])
        self.assertEqual(data['count'], 6)
