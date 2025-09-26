from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

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

class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='published')

    def for_seller(self, user: User):
        return self.filter(seller=user)

    def search_title(self, term: str):
        if not term:
            return self
        return self.filter(title__icontains=term)

    def by_category_id(self, category_id):
        if not category_id:
            return self
        return self.filter(category_id=category_id)

    def price_between(self, min_price, max_price):
        qs = self
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        return qs


class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Borrador'),
        ('published', 'Publicado'),
    ]
    
    objects = ProductQuerySet.as_manager()

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
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Calificación promedio")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.title} ({self.rating}/5) by {self.user.username}"

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
