from rest_framework import viewsets
from .models import Recipient, Message, Mailing, SendingAttempt
from .serializers import RecipientSerializer, MessageSerializer, MailingSerializer, SendingAttemptSerializer

class RecipientViewSet(viewsets.ModelViewSet):
    queryset = Recipient.objects.all()
    serializer_class = RecipientSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

class SendingAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SendingAttempt.objects.all()
    serializer_class = SendingAttemptSerializer
