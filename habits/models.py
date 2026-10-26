from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits'
    )
    action = models.CharField("Действие", max_length=255)
    location = models.CharField("Место", max_length=255, blank=True, default="")
    time = models.TimeField("Время выполнения")
    period_days = models.PositiveIntegerField("Периодичность (дни)", default=1)
    is_pleasant = models.BooleanField("Приятная привычка", default=False)
    reward = models.TextField("Вознаграждение", blank=True, null=True)
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_to',
        verbose_name="Связанная привычка"
    )
    execution_time_seconds = models.PositiveIntegerField("Время на выполнение (сек)", default=60)
    is_public = models.BooleanField("Публичная", default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        # ОСТАВЛЯЕМ ТОЛЬКО СЛОЖНЫЕ ПРОВЕРКИ, которые зависят от связей

        has_reward = bool(self.reward and self.reward.strip())
        has_related = bool(self.related_habit_id)

        # Нельзя одновременно reward и related_habit
        if has_reward and has_related:
            raise ValidationError("Можно указать либо вознаграждение, либо связанную привычку, но не оба одновременно.")

        # Приятная привычка не может иметь reward или related_habit
        if self.is_pleasant:
            if has_reward:
                raise ValidationError("Приятная привычка не может иметь вознаграждение.")
            if has_related:
                raise ValidationError("Приятная привычка не может иметь связанную привычку.")

        # Period_days от 1 до 7
        if not (1 <= self.period_days <= 7):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней включительно.")

        # Related_habit может быть только приятной привычкой
        if has_related and not self.related_habit.is_pleasant:
            raise ValidationError("Связанной привычкой может быть только приятная привычка.")

        # ПРОВЕРКУ execution_time_seconds УДАЛЯЕМ ОТСЮДА!
        # Она теперь только в сериализаторе.

    def save(self, *args, **kwargs):
        # Убираем full_clean() из save(), чтобы не дублировать логику и не ломать DRF
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} ({self.time})"
