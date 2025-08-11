from rest_framework import serializers
from .models import Idea, Message, Session

class IdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idea
        fields = ['id', 'title', 'description', 'created_at', 'metadata']
        read_only_fields = ['id', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'session', 'sender', 'content', 'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']

class SessionSerializer(serializers.ModelSerializer):
    idea = IdeaSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Session
        fields = ['id', 'idea', 'started_at', 'finished', 'agent_run_id', 
                 'report', 'report_sections', 'messages']
        read_only_fields = ['id', 'started_at', 'finished', 'agent_run_id', 
                           'report', 'report_sections']