from django.db import models
from decimal import Decimal


# Asosiy model
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        abstract = True


# Kategoriya modeli
class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['my_order']
        verbose_name = 'category'
        verbose_name_plural = "categories"


# Product modeli
class Product(BaseModel):
    class RatingChoice(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='media/products/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    stock = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    rating = models.PositiveIntegerField(choices=RatingChoice.choices, default=RatingChoice.ONE.value)

    @property
    def get_absolute_url(self):
        return self.image.url if self.image else None

    @property
    def discounted_price(self):
        if self.discount > 0:
            new_price = Decimal(self.price) * (Decimal(1) - Decimal(self.discount) / Decimal(100))
            return new_price.quantize(Decimal('0.01'))  # Narxni 2 xonali kasr sifatida saqlash
        return self.price

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['my_order']
        verbose_name = 'product'
        verbose_name_plural = 'products'


# Rasm modeli
class Img(BaseModel):
    image = models.ImageField(upload_to='media/img/')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}" if self.product else "No product"

    @property
    def get_absolute_url(self):
        return self.image.url if self.image else None


# Specification modeli
class Specification(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.product.name}" if self.product else self.name


# Attribute modeli
class Attribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# AttributeValue modeli
class AttributeValue(models.Model):
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


# ProductAttribute modeli
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_attributes', null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True, blank=True)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.attribute_value.value}"


# Customer modeli
class Customer(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
