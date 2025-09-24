from django.db import migrations

def create_default_categories(apps, schema_editor):
    """
    Crear categorías por defecto durante la migración
    """
    Category = apps.get_model('products', 'Category')
    
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
        Category.objects.create(
            name=cat_data['name'],
            description=cat_data['description']
        )

def reverse_create_default_categories(apps, schema_editor):
    """
    Revertir la creación de categorías por defecto
    """
    Category = apps.get_model('products', 'Category')
    Category.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_category_product_delete_movie'),
    ]

    operations = [
        migrations.RunPython(
            create_default_categories,
            reverse_create_default_categories
        ),
    ]
