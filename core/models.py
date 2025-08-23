from django.db import models

# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from core.auth import User




class Brand(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to="brand/", default="default.png")
    deleted = models.BooleanField(default=False)
    slug = models.SlugField(max_length=128)
    
    
    

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()
        self.brand_products.all().delete()

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug or self.name != Brand.objects.filter(pk=self.pk).values_list("name", flat=True).first():
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        
        
        
    class CustomManager(models.Manager):
        def all(self):
            return self.model.objects.filter(deleted=False)

        def get(self, *args, **kwargs):
            return self.model.objects.filter(deleted=False, *args, **kwargs).first()

    objects = CustomManager()
    
class Product(models.Model):
    name_ru = models.CharField(_("Название продукта (RU)"), max_length=50)
    name_en = models.CharField(_("Product name (EN)"), max_length=50)
    name_uz = models.CharField(_("Mahsulot nomi (UZ)"), max_length=50)
    name_ger = models.CharField(_("Produktname (Ger)"), max_length=50)
    
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name="brand_products")
    
    description_ru = models.TextField(_("Описание (RU)"), null=True, blank=True)
    description_en = models.TextField(_("Description (EN)"), null=True, blank=True)
    description_uz = models.TextField(_("Tavsif (UZ)"), null=True, blank=True)
    description_ger = models.TextField(_("Beschreibung (Ger)"), null=True, blank=True)
    
    price = models.IntegerField(_("Price"))
    
    price_type = models.CharField(max_length=3, choices=[
        ("UZS", "O'zbek so'mi"),
        ("USD", "Aqsh Dollori"),
        ("RUB", "Rossiya Rubli"),
    ], default="UZS")
    
    size = models.CharField(_("Size"), max_length=50, default=0)
    
    color_uz = models.CharField(_("Rang (UZ)"), max_length=50, null=True, blank=True)
    color_ru = models.CharField(_("Цвет (RU)"), max_length=50, null=True, blank=True)
    color_en = models.CharField(_("Color (EN)"), max_length=50, null=True, blank=True)
    color_ger = models.CharField(_("Farbe (GER)"), max_length=50, null=True, blank=True)
    
    discount = models.IntegerField(default=20)
    
    def get_price(self):
        return int(self.price * (1-self.discount/100))

    def get_price_with_icon(self):
        price = {
            "USD": f"{self.get_price()} $",
            "RUB": f"{self.get_price()} ₽",
            "UZS": f"{self.get_price()} So'm",
        }
        return price[self.price_type]
    
    def get_price_original_with_icon(self):
        price = {
            "USD": f"{self.price} $",
            "RUB": f"{self.price} ₽",
            "UZS": f"{self.price} So'm",
        }
        return price[self.price_type]

    
    
    def get_color(self, lang="uz"):
        if lang == "ru":
            return self.color_ru
        elif lang == "en":
            return self.color_en
        elif lang == "uz":
            return self.color_uz
        elif lang == "ger":
            return self.color_ger
        return self.color_ru 
    
    def get_name(self, lang="uz"):
        if lang == "ru":
            return self.name_ru
        elif lang == "en":
            return self.name_en
        elif lang == "uz":
            return self.name_uz
        elif lang == "ger":
            return self.name_ger
        return self.name_ru 
    
    def get_desc(self, lang="uz"):
        if lang == "ru":
            return self.description_ru
        elif lang == "en":
            return self.description_en
        elif lang == "uz":
            return self.description_uz
        elif lang == "ger":
            return self.description_ger
        return self.description_ru 
    

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.product.name_ru}"
    

class Cart(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="carts"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0, editable=False)
    status = models.BooleanField(default=True) 

    def save(self, *args, **kwargs):
        self.total_price = self.product.get_price() * self.quantity
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} → {self.product.name_ru} x {self.quantity}"







class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    email = models.EmailField(_("Email"))
    full_name = models.CharField(_("Полное имя"), max_length=255)
    phone = models.CharField(_("Телефон"), max_length=12)
    additional_info = models.TextField(_("Примечания"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cart_items = models.ManyToManyField(Cart, related_name="orders")

    def get_total_price(self):
        return sum(item.total_price for item in self.cart_items.all())

    def __str__(self):
        return f"Заказ #{self.id} от {self.user or 'Anonymous'}"

    

