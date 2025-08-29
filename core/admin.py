from django.contrib import admin
from core.models import Brand, CarModel, CarYear, CarSeries, Product, ProductImage, Cart, Order


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'deleted')
    list_filter = ('deleted',)
    search_fields = ('name',)
    list_per_page = 20


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'deleted')
    list_filter = ('brand', 'deleted')
    search_fields = ('name', 'brand__name')
    list_per_page = 20


@admin.register(CarYear)
class CarYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'model', 'deleted')
    list_filter = ('model__brand', 'deleted')
    search_fields = ('year', 'model__name', 'model__brand__name')
    list_per_page = 20


@admin.register(CarSeries)
class CarSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'deleted')
    list_filter = ('year__model__brand', 'deleted')
    search_fields = ('name', 'year__year', 'year__model__name', 'year__model__brand__name')
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'brand', 'car_model', 'car_year', 'car_series',
                    'get_price_with_icon', 'discount', 'deleted')
    list_filter = ('brand', 'car_model', 'car_year', 'car_series', 'price_type', 'deleted')
    search_fields = ('name_ru', 'name_en', 'name_uz', 'name_ger',
                     'brand__name', 'car_model__name')
    list_per_page = 20


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product',)
    list_filter = ('product__brand',)
    search_fields = ('product__name_ru', 'product__name_en')
    list_per_page = 20


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'product__name_ru')
    list_per_page = 20


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'email', 'phone')
    list_per_page = 20
