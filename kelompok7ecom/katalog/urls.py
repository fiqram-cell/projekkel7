from django.urls import path
from . import views
from .views import custom_login

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('', views.home, name='home'),
    path('login/', custom_login, name='login'),
    # URL lainnya
]