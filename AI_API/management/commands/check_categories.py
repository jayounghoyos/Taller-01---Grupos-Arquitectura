"""
Comando para verificar las categorías disponibles en la base de datos
"""
from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Verifica las categorías disponibles en la base de datos'

    def handle(self, *args, **options):
        categories = Category.objects.all()
        
        if not categories.exists():
            self.stdout.write(
                self.style.WARNING('No hay categorías en la base de datos')
            )
            self.stdout.write('Creando categorías por defecto...')
            
            # Crear categorías por defecto
            default_categories = [
                'Ropa',
                'Electrónicos', 
                'Hogar',
                'Deportes',
                'Libros',
                'Juguetes',
                'Belleza',
                'Automotriz',
                'Jardín',
                'Oficina'
            ]
            
            for cat_name in default_categories:
                category, created = Category.objects.get_or_create(
                    name=cat_name,
                    defaults={'description': f'Categoría de {cat_name.lower()}'}
                )
                if created:
                    self.stdout.write(f'✓ Creada categoría: {cat_name}')
                else:
                    self.stdout.write(f'- Categoría ya existe: {cat_name}')
        else:
            self.stdout.write(
                self.style.SUCCESS('Categorías disponibles:')
            )
            for category in categories:
                self.stdout.write(f'  - {category.name} (ID: {category.id})')
        
        self.stdout.write('\nPara que la IA pueda seleccionar categorías automáticamente,')
        self.stdout.write('asegúrate de que las categorías en la base de datos coincidan')
        self.stdout.write('con las sugeridas por la IA.')
