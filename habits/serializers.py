from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id',
            'action',
            'time',
            'period_days',
            'execution_time_seconds',
            'is_pleasant',
        ]

    def validate_execution_time_seconds(self, value):
        if value > 120:
            raise serializers.ValidationError("Время на выполнение не может превышать 120 секунд.")
        return value

