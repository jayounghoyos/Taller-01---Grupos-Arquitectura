from rest_framework import serializers
from .models import AIRequest, AIConfiguration
from django.contrib.auth.models import User


class AIRequestSerializer(serializers.ModelSerializer):
    """
    Serializer para requests de IA
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    has_images = serializers.BooleanField(read_only=True)
    is_multimodal = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = AIRequest
        fields = [
            'id', 'user', 'user_username', 'request_type', 'status',
            'prompt', 'image_urls', 'model_name', 'max_tokens', 'temperature',
            'response_text', 'response_tokens', 'processing_time',
            'created_at', 'updated_at', 'error_message',
            'has_images', 'is_multimodal'
        ]
        read_only_fields = [
            'id', 'user', 'status', 'response_text', 'response_tokens',
            'processing_time', 'created_at', 'updated_at', 'error_message',
            'has_images', 'is_multimodal'
        ]


class AIConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer para configuración de IA
    """
    class Meta:
        model = AIConfiguration
        fields = [
            'id', 'name', 'lightning_endpoint', 'api_key',
            'model_name', 'max_tokens_default', 'temperature_default',
            'timeout_seconds', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer básico para usuarios
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']
