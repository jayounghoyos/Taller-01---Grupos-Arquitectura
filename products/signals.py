from django.db.models.signals import post_migrate, post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.db.models import Avg
from .models import Category, Review, Product

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


def _recompute_product_average(product_id: int):
    try:
        product = Product.objects.get(id=product_id)
        avg = product.reviews.aggregate(v=Avg('rating'))['v'] or 0
        product.average_rating = round(float(avg), 2)
        product.save(update_fields=['average_rating'])
    except Product.DoesNotExist:
        pass


@receiver(post_save, sender=Review)
def on_review_saved(sender, instance: Review, created, **kwargs):
    _recompute_product_average(instance.product_id)


@receiver(post_delete, sender=Review)
def on_review_deleted(sender, instance: Review, **kwargs):
    _recompute_product_average(instance.product_id)
