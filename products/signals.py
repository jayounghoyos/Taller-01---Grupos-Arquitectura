from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from .models import Category

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    """
    Crea categorías por defecto después de cada migración
    Solo se ejecuta si no existen categorías
    """
    # Verificar si ya existen categorías
    if Category.objects.exists():
        return
    
    # Categorías por defecto
    default_categories = [
        {
            'name': 'Electrónica',
            'description': 'Productos electrónicos y tecnológicos'
        },
        {
            'name': 'Ropa',
            'description': 'Vestimenta y accesorios'
        },
        {
            'name': 'Hogar',
            'description': 'Artículos para el hogar y decoración'
        },
        {
            'name': 'Deportes',
            'description': 'Equipamiento y ropa deportiva'
        },
        {
            'name': 'Libros',
            'description': 'Libros, revistas y material educativo'
        },
        {
            'name': 'Juguetes',
            'description': 'Juguetes y entretenimiento'
        },
        {
            'name': 'Automóviles',
            'description': 'Partes y accesorios para vehículos'
        },
        {
            'name': 'Jardín',
            'description': 'Productos para jardín y exteriores'
        },
        {
            'name': 'Salud y Belleza',
            'description': 'Productos de cuidado personal y belleza'
        },
        {
            'name': 'Mascotas',
            'description': 'Productos para mascotas y animales'
        }
    ]
    
    # Crear categorías
    for cat_data in default_categories:
        Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
    
    print(f"✅ {len(default_categories)} categorías creadas automáticamente")
