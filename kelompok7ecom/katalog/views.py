from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Cart, CartItem, Order, OrderItem

# Menampilkan Daftar Produk
def product_list(request):
    categories = Category.objects.all()  # Ambil semua kategori produk
    products = Product.objects.all()  # Ambil semua produk
    return render(request, 'katalog/product_list.html', {'categories': categories, 'products': products})

# Menampilkan Detail Produk berdasarkan slug
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)  # Ambil produk berdasarkan slug
    return render(request, 'katalog/product_detail.html', {'product': product})

# Menambah produk ke dalam keranjang
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Ambil produk berdasarkan ID
    cart, created = Cart.objects.get_or_create(user=request.user)  # Ambil atau buat keranjang untuk user
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)  # Ambil atau buat item keranjang
    if not created:  # Jika produk sudah ada di keranjang, tambahkan kuantitas
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')  # Redirect ke halaman keranjang

# Menampilkan detail keranjang
@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)# Ambil keranjang berdasarkan user
    return render(request, 'katalog/cart_detail.html', {'cart': cart})

# Proses checkout dan buat pesanan
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)  # Ambil keranjang untuk user
    order = Order.objects.create(
        user=request.user, 
        total_amount=sum(item.product.price * item.quantity for item in cart.cartitem_set.all())  # Hitung total harga
    )
    
    # Buat item pesanan untuk setiap item dalam keranjang
    for item in cart.cartitem_set.all():
        OrderItem.objects.create(
            order=order, 
            product=item.product, 
            quantity=item.quantity, 
            price=item.product.price
        )
    
    cart.cartitem_set.all().delete()  # Kosongkan keranjang setelah checkout
    return render(request, 'katalog/order_confirmation.html', {'order': order})  # Tampilkan konfirmasi pesanan

def home(request):
    return render(request, 'katalog/home.html')

from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect ke home setelah login
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

