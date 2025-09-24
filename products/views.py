from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm
from django.contrib.auth.models import User
from .models import Product, Category, Wishlist


def home(request):
    searchTerm = request.GET.get('searchProduct')
    category_filter = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    
    products = Product.objects.filter(status='published')
    
    if searchTerm:
        products = products.filter(title__icontains=searchTerm)
    
    if category_filter:
        products = products.filter(category_id=category_filter)
    
    if price_min:
        products = products.filter(price__gte=price_min)
    
    if price_max:
        products = products.filter(price__lte=price_max)
    
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'searchTerm': searchTerm,
        'categories': categories,
        'selected_category': category_filter,
        'price_min': price_min,
        'price_max': price_max
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Producto creado exitosamente!')
            return redirect('home')
    else:
        form = ProductForm()
    
    # Obtener todas las categorías para el formulario
    categories = Category.objects.all()
    
    return render(request, 'create_product.html', {'form': form, 'categories': categories})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente!')
            return redirect('home')
    else:
        form = ProductForm(instance=product)
    
    # Obtener todas las categorías para el formulario
    categories = Category.objects.all()
    
    return render(request, 'edit_product.html', {'form': form, 'product': product, 'categories': categories})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto eliminado exitosamente!')
        return redirect('home')
    
    return render(request, 'delete_product.html', {'product': product})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    return render(request, 'product_detail.html', {
        'product': product,
        'in_wishlist': in_wishlist
    })

def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk, status='published')
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

@login_required
def my_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

    if not created:
        wishlist_item.delete()  # si ya existía, se elimina (toggle)
    return redirect('product_detail', pk=pk)

@login_required
def my_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, 'my_wishlist.html', {"wishlist_items": wishlist_items})

@login_required
def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)

    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        # Si ya existía, lo quitamos
        wishlist_item.delete()

    return redirect('product_detail', pk=pk)


def profile(request):
    profile = request.user
    return render(request, 'profile.html', {'profile': profile})

def products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'products.html', {'products': products})
