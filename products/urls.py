from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('product/create/', views.create_product, name='create_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('products/',views.products, name='products'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile' ),

    path('about/', views.about, name='about'),
    
    path('wishlist/<int:pk>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', views.my_wishlist, name='my_wishlist'),
    path('wishlist/toggle/<int:pk>/', views.toggle_wishlist, name='toggle_wishlist'),



]
