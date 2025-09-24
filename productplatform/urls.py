"""
URL configuration for productplatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', other_app.views.Home, name='home')
Including another URLconf
    1. Import the include function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from products import views as productViews
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', productViews.home, name='home'),
    path('about/', productViews.about, name='about'),
    path('register/', productViews.register, name='register'),
    path('login/', productViews.user_login, name='login'),
    path('logout/', productViews.user_logout, name='logout'),
    path('product/create/', productViews.create_product, name='create_product'),
    path('product/<int:pk>/edit/', productViews.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', productViews.delete_product, name='delete_product'),
    path('product/<int:pk>/', productViews.product_detail, name='product_detail'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('', include('products.urls')),
    
    # AI API endpoints
    path('api/ai/', include('AI_API.urls')),
    path('ai-dashboard/', include('AI_API.urls', namespace='ai_dashboard')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)