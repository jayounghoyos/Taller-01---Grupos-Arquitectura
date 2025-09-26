from django.urls import path
from . import views
from .views import (
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDetailView,
    SubmitReviewView,
)

urlpatterns = [
    path('', views.home, name='home'),

    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/review/', SubmitReviewView.as_view(), name='submit_review'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='edit_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
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
