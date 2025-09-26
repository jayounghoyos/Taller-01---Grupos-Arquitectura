
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    
    # AI API endpoints
    path('api/ai/', include('AI_API.urls')),
    path('ai-dashboard/', include('AI_API.urls', namespace='ai_dashboard')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)