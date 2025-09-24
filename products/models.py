from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

#Tags for products
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(2)])
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Título del producto")
    description = models.TextField(verbose_name="Descripción")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoría")
    image = models.ImageField(upload_to='products/images/', verbose_name="Imagen del producto")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Vendedor")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Borrador', verbose_name="Estado")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Etiquetas")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        verbose_name = "Lista de deseos"
        verbose_name_plural = "Listas de deseos"

    def __str__(self):
        return f"{self.user.username} → {self.product.title}"
