from rest_framework import serializers
from .models import Recipient, Message, Mailing, SendingAttempt

class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = '__all__'

class SendingAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendingAttempt
        fields = '__all__'
