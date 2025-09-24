from django.urls import path
from . import views

app_name = 'ai_api'

# URLs principales de la API de IA
urlpatterns = [
    # Endpoints principales
    path('health/', views.health_check, name='health_check'),
    path('analyze-product/', views.analyze_product_image_upload, name='analyze_product_image_upload'),
]
