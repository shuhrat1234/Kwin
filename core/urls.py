from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('basket/', views.basket, name='basket'),
    path('set-language/<str:lang>/', views.set_language, name='set_language'),
    path("cart/add/<int:add_id>/", views.cart_add, name="cart-add"),
    path('cart/remove/<int:remove_id>/', views.cart_remove, name='cart-remove'),
    path('ch/cart/<int:cart_id>/<int:inc>/', views.change_cart, name='change_cart'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/order/', views.order_create, name='order_create'),
    path('products/', views.products, name='products'),
    path('reset_filters/', views.reset_filters, name='reset_filters'),
    path('get_models/', views.get_models, name='get_models'),
    path('get_years/', views.get_years, name='get_years'),
    path('get_series/', views.get_series, name='get_series'),
]

