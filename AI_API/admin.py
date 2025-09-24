from django.contrib import admin
from .models import AIRequest, AIConfiguration


@admin.register(AIRequest)
class AIRequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'request_type', 'status', 'model_name',
        'response_tokens', 'processing_time', 'created_at'
    ]
    list_filter = ['request_type', 'status', 'model_name', 'created_at']
    search_fields = ['prompt', 'response_text', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'processing_time']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'request_type', 'status', 'model_name')
        }),
        ('Request', {
            'fields': ('prompt', 'image_urls', 'max_tokens', 'temperature')
        }),
        ('Response', {
            'fields': ('response_text', 'response_tokens', 'processing_time', 'error_message')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AIConfiguration)
class AIConfigurationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'model_name', 'lightning_endpoint', 'is_active',
        'max_tokens_default', 'temperature_default'
    ]
    list_filter = ['is_active', 'model_name']
    search_fields = ['name', 'lightning_endpoint']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Configuración', {
            'fields': ('name', 'is_active')
        }),
        ('Endpoint', {
            'fields': ('lightning_endpoint', 'api_key')
        }),
        ('Modelo', {
            'fields': ('model_name', 'max_tokens_default', 'temperature_default', 'timeout_seconds')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ProductAIGenerationAdmin eliminado - no necesario para funcionalidad básica