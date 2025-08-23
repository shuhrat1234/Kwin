from django.contrib import admin

from core.models import Brand, Order, Product, ProductImage

# Register your models here.


admin.site.register(Brand)
admin.site.register(ProductImage)
admin.site.register(Product)
admin.site.register(Order)

