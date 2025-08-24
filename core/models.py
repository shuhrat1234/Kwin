from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from core.auth import User
class BrandQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(deleted=False)


class BrandManager(models.Manager):
    def get_queryset(self):
        return BrandQuerySet(self.model, using=self._db).alive()
class Brand(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to="brand/", default="default.png")
    deleted = models.BooleanField(default=False)
    slug = models.SlugField(max_length=128, unique=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()
        self.brand_products.all().delete()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # если slug пустой
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # пока существует бренд с таким slug — добавляем суффикс
            while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=128)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.brand.name} {self.name}"

class CarYear(models.Model):
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="years", null=True, blank=True)
    year = models.PositiveIntegerField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.model} {self.year}"

class CarSeries(models.Model):
    year = models.ForeignKey(CarYear, on_delete=models.CASCADE, related_name="series", null=True, blank=True)
    name = models.CharField(max_length=128)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.year} {self.name}"

class Product(models.Model):
    name_ru = models.CharField(_("Название продукта (RU)"), max_length=50)
    name_en = models.CharField(_("Product name (EN)"), max_length=50)
    name_uz = models.CharField(_("Mahsulot nomi (UZ)"), max_length=50)
    name_ger = models.CharField(_("Produktname (Ger)"), max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name="brand_products")
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, null=True, blank=True)
    car_year = models.ForeignKey(CarYear, on_delete=models.CASCADE, null=True, blank=True)
    car_series = models.ForeignKey(CarSeries, on_delete=models.CASCADE, null=True, blank=True)
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
    size = models.CharField(_("Size"), max_length=50, default="0")
    color_uz = models.CharField(_("Rang (UZ)"), max_length=50, null=True, blank=True)
    color_ru = models.CharField(_("Цвет (RU)"), max_length=50, null=True, blank=True)
    color_en = models.CharField(_("Color (EN)"), max_length=50, null=True, blank=True)
    color_ger = models.CharField(_("Farbe (GER)"), max_length=50, null=True, blank=True)
    discount = models.IntegerField(default=20)
    deleted = models.BooleanField(default=False)

    def get_price(self):
        return int(self.price * (1 - self.discount / 100))

    def __str__(self):
        return self.name_en
    
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
        return getattr(self, f"color_{lang}", self.color_ru)

    def get_name(self, lang="uz"):
        return getattr(self, f"name_{lang}", self.name_ru)

    def get_desc(self, lang="uz"):
        return getattr(self, f"description_{lang}", self.description_ru)

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.product.name_ru}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=0, editable=False)
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.total_price = self.product.get_price() * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} → {self.product.name_ru} x {self.quantity}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    email = models.EmailField(_("Email"))
    full_name = models.CharField(_("Полное имя"), max_length=255, default="")
    phone = models.CharField(_("Телефон"), max_length=12, default="")
    additional_info = models.TextField(_("Примечания"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.product.get_price() * self.quantity

    def __str__(self):
        return f"Заказ #{self.id} от {self.user or 'Anonymous'}"