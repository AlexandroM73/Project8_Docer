from rest_framework.routers import DefaultRouter
from .views import RecipientViewSet, MessageViewSet, MailingViewSet, SendingAttemptViewSet

router = DefaultRouter()
router.register(r'recipients', RecipientViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'mailings', MailingViewSet)
router.register(r'attempts', SendingAttemptViewSet, basename='attempt')
