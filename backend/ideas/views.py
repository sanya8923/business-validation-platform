import hmac, hashlib, json, os
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Idea, Session, Message, Subscription
from .serializers import IdeaSerializer, MessageSerializer, SessionSerializer
from .agent_client import AgentClient
from django.db import transaction
from .tasks import start_session_task, send_user_message_task
from django.conf import settings

def verify_agent_signature(request):
    secret = getattr(settings, 'AGENT_CALLBACK_SECRET', None)
    if not secret:
        return False
    sig = request.headers.get('X-Agent-Signature') or request.headers.get('X-Agent-Signature'.lower())
    if not sig:
        return False
    body = request.body or b''
    mac = hmac.new(secret.encode('utf-8'), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, sig)

class IdeaViewSet(viewsets.ModelViewSet):
    serializer_class = IdeaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Idea.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        has_subscription = getattr(user, 'subscription', None) and user.subscription.active
        if not has_subscription:
            one_month_ago = timezone.now() - timedelta(days=30)
            recent = Idea.objects.filter(owner=user, created_at__gte=one_month_ago).exists()
            if recent:
                return Response({
                    "detail": "Free quota exhausted: only 1 idea per 30 days. Buy a subscription to continue."
                }, status=status.HTTP_402_PAYMENT_REQUIRED)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            idea = serializer.save(owner=user)
            session = Session.objects.create(idea=idea)
            # start async task
            start_session_task.delay(session.id)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(session__idea__owner=self.request.user)

    def create(self, request, *args, **kwargs):
        session_id = request.data.get('session')
        session = get_object_or_404(Session, pk=session_id, idea__owner=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        msg = serializer.save()
        # forward to agents async
        send_user_message_task.delay(session.id, msg.id)
        return Response(self.get_serializer(msg).data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def agent_callback(request):
    # Verify signature
    if not verify_agent_signature(request):
        return Response({'error': 'invalid signature'}, status=401)

    payload = request.data
    sid = payload.get('session_id')
    try:
        session = Session.objects.get(pk=sid)
    except Session.DoesNotExist:
        return Response({"error": "session not found"}, status=404)

    Message.objects.create(
        session=session,
        sender=Message.SENDER_AGENT,
        content=payload.get('content', ''),
        metadata=payload.get('metadata', {})
    )

    if payload.get('type') == 'final_report':
        session.report = payload.get('report_html', '')
        session.report_sections = payload.get('report_sections', [])
        session.finished = True
        session.save()

    return Response({"status": "ok"})

# Stripe-stub endpoints (simple)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stripe_start_subscription(request):
    # In real life redirect to Stripe checkout. Here, just activate subscription immediately.
    user = request.user
    sub, _ = Subscription.objects.get_or_create(user=user)
    sub.active = True
    sub.plan = request.data.get('plan', 'pro')
    sub.started_at = timezone.now()
    sub.save()
    return Response({'status': 'subscribed'})

@api_view(['POST'])
@permission_classes([AllowAny])
def stripe_webhook_stub(request):
    # Accepts {"user": username, "action": "subscribe"|"cancel"}
    payload = request.data or {}
    username = payload.get('user')
    action = payload.get('action')
    if not username or not action:
        return Response({'error': 'bad payload'}, status=400)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'user not found'}, status=404)
    sub, _ = Subscription.objects.get_or_create(user=u)
    if action == 'subscribe':
        sub.active = True
        sub.started_at = timezone.now()
    elif action == 'cancel':
        sub.active = False
    sub.save()
    return Response({'status': 'ok'})