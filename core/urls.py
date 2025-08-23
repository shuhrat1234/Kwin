from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('basket/', views.basket, name='basket'),
    path('set-language/<str:lang>/', views.set_language, name='set_language'),
    path("add-to-cart/<int:add_id>/", views.basket, name="cart-add"),
    path("ch/cart/<int:cart_id>/<int:inc>/", views.change_cart, name='change_cart'),
    path('cart/add/<int:add_id>/', views.cart_add, name='cart-add'),
    path('cart/remove/<int:remove_id>/', views.cart_remove, name='cart-remove'),
    
    
    
    
    
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]