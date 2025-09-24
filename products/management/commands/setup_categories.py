from django.core.management.base import BaseCommand
from products.models import Category
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Configura categorías por defecto y usuario de ejemplo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar recreación de categorías existentes',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        # Crear categorías por defecto
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
        
        # Crear o actualizar categorías
        categories_created = 0
        categories_updated = 0
        
        for cat_data in default_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            
            if created:
                categories_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Categoría creada: {category.name}')
                )
            else:
                if force:
                    category.description = cat_data['description']
                    category.save()
                    categories_updated += 1
                    self.stdout.write(
                        self.style.WARNING(f'🔄 Categoría actualizada: {category.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f'ℹ️  Categoría ya existe: {category.name}')
                    )
        
        # Crear usuario de ejemplo si no existe
        user, created = User.objects.get_or_create(
            username='usuario_ejemplo',
            defaults={
                'email': 'ejemplo@test.com',
                'first_name': 'Usuario',
                'last_name': 'Ejemplo'
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS('✅ Usuario de ejemplo creado: usuario_ejemplo / password123')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('ℹ️  Usuario de ejemplo ya existe')
            )
        
        # Resumen final
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Configuración completada!\n'
                f'📊 Categorías creadas: {categories_created}\n'
                f'🔄 Categorías actualizadas: {categories_updated}\n'
                f'📦 Total de categorías: {Category.objects.count()}\n'
                f'👥 Total de usuarios: {User.objects.count()}'
            )
        )
