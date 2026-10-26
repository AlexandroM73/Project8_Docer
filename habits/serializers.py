from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'action', 'location', 'time', 'period_days',
            'is_pleasant', 'reward', 'related_habit', 'execution_time_seconds',
            'is_public', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'user': {'required': False}
        }

    def validate_execution_time_seconds(self, value):
        if value > 120:
            raise serializers.ValidationError("Время выполнения не может превышать 120 секунд.")
        return value
