from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IdeaViewSet, MessageViewSet, agent_callback, stripe_start_subscription, stripe_webhook_stub

router = DefaultRouter()
router.register(r'ideas', IdeaViewSet, basename='idea')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('agents/callback/', agent_callback, name='agent-callback'),
    path('stripe/start/', stripe_start_subscription, name='stripe-start'),
    path('stripe/webhook/', stripe_webhook_stub, name='stripe-webhook'),
]