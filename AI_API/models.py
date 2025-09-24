from django.db import models
from django.contrib.auth.models import User


class AIRequest(models.Model):
    """
    Modelo para almacenar las requests realizadas al modelo Gemma 3
    """
    REQUEST_TYPES = [
        ('product_description', 'Descripción de Producto'),
        ('image_analysis', 'Análisis de Imagen'),
        ('text_generation', 'Generación de Texto'),
        ('chat', 'Chat Conversacional'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES, default='chat')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Datos de entrada
    prompt = models.TextField(help_text="Prompt o texto enviado al modelo")
    image_urls = models.JSONField(default=list, blank=True, help_text="URLs de imágenes enviadas")
    model_name = models.CharField(max_length=100, default='google/gemma-3-4b-it')
    max_tokens = models.IntegerField(default=256)
    temperature = models.FloatField(default=0.7)
    
    # Datos de respuesta
    response_text = models.TextField(blank=True, null=True)
    response_tokens = models.IntegerField(default=0)
    processing_time = models.FloatField(default=0.0, help_text="Tiempo de procesamiento en segundos")
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'AI Request'
        verbose_name_plural = 'AI Requests'
    
    def __str__(self):
        return f"AI Request {self.id} - {self.request_type} - {self.status}"
    
    @property
    def has_images(self):
        return len(self.image_urls) > 0
    
    @property
    def is_multimodal(self):
        return self.has_images and self.prompt


# Eliminado AIUsageStats - No necesario para funcionalidad básica


class AIConfiguration(models.Model):
    """
    Modelo para configuraciones del servicio de IA
    """
    name = models.CharField(max_length=100, unique=True)
    lightning_endpoint = models.URLField(help_text="URL del endpoint de Lightning AI")
    api_key = models.CharField(max_length=200, help_text="API Key para autenticación")
    model_name = models.CharField(max_length=100, default='google/gemma-3-4b-it')
    max_tokens_default = models.IntegerField(default=256)
    temperature_default = models.FloatField(default=0.7)
    timeout_seconds = models.IntegerField(default=300)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'AI Configuration'
        verbose_name_plural = 'AI Configurations'
    
    def __str__(self):
        return f"AI Config: {self.name} - {'Active' if self.is_active else 'Inactive'}"


# Eliminado ProductAIGeneration - No necesario para funcionalidad básica