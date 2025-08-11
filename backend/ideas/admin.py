from django.contrib import admin
from .models import Idea, Session, Message, Subscription

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'active', 'plan', 'started_at']
    list_filter = ['active', 'plan']
    search_fields = ['user__username', 'user__email']

@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description', 'owner__username']
    readonly_fields = ['created_at']

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['idea', 'started_at', 'finished', 'agent_run_id']
    list_filter = ['finished', 'started_at']
    search_fields = ['idea__title', 'agent_run_id']
    readonly_fields = ['started_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'sender', 'created_at', 'content_preview']
    list_filter = ['sender', 'created_at']
    search_fields = ['content', 'session__idea__title']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'