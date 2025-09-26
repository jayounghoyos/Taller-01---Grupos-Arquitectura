from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm, ReviewForm
from django.contrib.auth.models import User
from .models import Product, Category, Wishlist
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    searchTerm = request.GET.get('searchProduct')
    category_filter = request.GET.get('category')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    products = (
        Product.objects
        .published()
        .search_title(searchTerm)
        .by_category_id(category_filter)
        .price_between(price_min, price_max)
    )

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

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'create_product.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.seller = self.request.user
        obj.save()
        messages.success(self.request, 'Producto creado exitosamente!')
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'edit_product.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Product.objects.for_seller(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado exitosamente!')
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'delete_product.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Product.objects.for_seller(self.request.user)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        in_wishlist = False
        if self.request.user.is_authenticated:
            in_wishlist = Wishlist.objects.filter(user=self.request.user, product=self.object).exists()
        ctx['in_wishlist'] = in_wishlist
        ctx['review_form'] = ReviewForm()
        ctx['reviews'] = self.object.reviews.select_related('user')
        return ctx


class SubmitReviewView(LoginRequiredMixin, FormView):
    form_class = ReviewForm

    def form_valid(self, form):
        from .models import Review
        product = get_object_or_404(Product, pk=self.kwargs['pk'])

        # Moderation strategy (simple): basic profanity filter / length check
        comment = form.cleaned_data.get('comment', '')
        rating = form.cleaned_data['rating']
        if any(bad in (comment or '').lower() for bad in ['spam', 'http://', 'https://']):
            messages.error(self.request, 'Tu reseña parece contener spam o enlaces no permitidos.')
            return redirect('product_detail', pk=product.pk)

        Review.objects.update_or_create(
            product=product,
            user=self.request.user,
            defaults={
                'rating': rating,
                'comment': comment,
            }
        )
        messages.success(self.request, '¡Gracias por tu reseña!')
        return redirect('product_detail', pk=product.pk)

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
