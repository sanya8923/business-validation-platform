from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import JSONField

User = settings.AUTH_USER_MODEL

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    active = models.BooleanField(default=False)
    plan = models.CharField(max_length=100, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Subscription({self.user}, active={self.active})"

class Idea(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ideas')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.title

class Session(models.Model):
    idea = models.OneToOneField(Idea, on_delete=models.CASCADE, related_name='session')
    started_at = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)
    agent_run_id = models.CharField(max_length=255, blank=True, null=True)
    report = models.TextField(blank=True)
    report_sections = JSONField(default=list, blank=True)

    def __str__(self):
        return f"Session({self.idea_id})"

class Message(models.Model):
    SENDER_USER = 'user'
    SENDER_AGENT = 'agent'
    SENDER_SYSTEM = 'system'
    SENDER_CHOICES = [
        (SENDER_USER, 'User'),
        (SENDER_AGENT, 'Agent'),
        (SENDER_SYSTEM, 'System'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    content = models.TextField()
    metadata = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message({self.sender}, {self.created_at})"