from django.contrib import admin
from core.models import Brand, CarModel, CarYear, CarSeries, Order, Product, ProductImage, Cart


# Inline for ProductImage to be used in ProductAdmin
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image',)
    readonly_fields = ('image',)
    can_delete = True


# Inline for CarModel to be used in BrandAdmin
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1
    fields = ('name', 'deleted')
    readonly_fields = ('name',)
    can_delete = True


# Inline for CarYear to be used in CarModelAdmin
class CarYearInline(admin.TabularInline):
    model = CarYear
    extra = 1
    fields = ('year', 'deleted')
    readonly_fields = ('year',)
    can_delete = True


# Inline for CarSeries to be used in CarYearAdmin
class CarSeriesInline(admin.TabularInline):
    model = CarSeries
    extra = 1
    fields = ('name', 'deleted')
    readonly_fields = ('name',)
    can_delete = True


# Inline for Cart to be used in OrderAdmin
class CartInline(admin.TabularInline):
    model = Cart
    extra = 0
    fields = ('product', 'quantity', 'total_price', 'status')
    readonly_fields = ('product', 'quantity', 'total_price', 'status')
    can_delete = False


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'deleted')
    list_filter = ('deleted',)
    search_fields = ('name',)
    list_per_page = 20
    inlines = [CarModelInline]
    prepopulated_fields = {'slug': ('name',)}
    actions = ['soft_delete', 'restore']

    def soft_delete(self, request, queryset):
        queryset.update(deleted=True)
    soft_delete.short_description = "Mark selected brands as deleted"

    def restore(self, request, queryset):
        queryset.update(deleted=False)
    restore.short_description = "Restore selected brands"


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'deleted')
    list_filter = ('brand', 'deleted')
    search_fields = ('name', 'brand__name')
    list_per_page = 20
    inlines = [CarYearInline]
    actions = ['soft_delete', 'restore']

    def soft_delete(self, request, queryset):
        queryset.update(deleted=True)
    soft_delete.short_description = "Mark selected models as deleted"

    def restore(self, request, queryset):
        queryset.update(deleted=False)
    restore.short_description = "Restore selected models"


@admin.register(CarYear)
class CarYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'model', 'deleted')
    list_filter = ('model__brand', 'deleted')
    search_fields = ('year', 'model__name', 'model__brand__name')
    list_per_page = 20
    inlines = [CarSeriesInline]
    actions = ['soft_delete', 'restore']

    def soft_delete(self, request, queryset):
        queryset.update(deleted=True)
    soft_delete.short_description = "Mark selected years as deleted"

    def restore(self, request, queryset):
        queryset.update(deleted=False)
    restore.short_description = "Restore selected years"


@admin.register(CarSeries)
class CarSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'model', 'brand', 'deleted')
    list_filter = ('year__model__brand', 'deleted')
    search_fields = ('name', 'year__year', 'year__model__name', 'year__model__brand__name')
    list_per_page = 20
    actions = ['soft_delete', 'restore']

    def model(self, obj):
        return obj.year.model
    model.short_description = 'Model'

    def brand(self, obj):
        return obj.year.model.brand
    brand.short_description = 'Brand'

    def soft_delete(self, request, queryset):
        queryset.update(deleted=True)
    soft_delete.short_description = "Mark selected series as deleted"

    def restore(self, request, queryset):
        queryset.update(deleted=False)
    restore.short_description = "Restore selected series"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'brand', 'car_model', 'car_year', 'car_series', 'get_price_with_icon', 'discount', 'deleted')
    list_filter = ('brand', 'car_model', 'car_year', 'car_series', 'price_type', 'deleted')
    search_fields = ('name_ru', 'name_en', 'name_uz', 'name_ger', 'brand__name', 'car_model__name')
    list_per_page = 20
    inlines = [ProductImageInline]
    list_editable = ('discount',)
    actions = ['soft_delete', 'restore']

    def soft_delete(self, request, queryset):
        queryset.update(deleted=True)
    soft_delete.short_description = "Mark selected products as deleted"

    def restore(self, request, queryset):
        queryset.update(deleted=False)
    restore.short_description = "Restore selected products"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product',)
    list_filter = ('product__brand',)
    search_fields = ('product__name_ru', 'product__name_en')
    list_per_page = 20

