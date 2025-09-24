from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    verbose_name = 'Gestión de Productos'
    
    def ready(self):
        """Importar signals cuando la app esté lista"""
        import products.signals
