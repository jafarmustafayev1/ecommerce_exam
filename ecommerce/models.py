from django.db import models
from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField
import random
import string
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

# Bazaviy model (barcha modellarga qo‘shiladigan umumiy maydonlar)
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['my_order']
        verbose_name = 'category'
        verbose_name_plural = "categories"


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    stock = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)

    @property
    def get_absolute_url(self):
        primary_images = self.product_images.filter(is_primary=True)
        if primary_images.exists():
            return primary_images.first().image.url
        return "products/default_image.jpg"

    @property
    def discounted_price(self):
        new_price = self.price
        if self.discount > 0:
            new_price = Decimal(self.price) * Decimal((1 - self.discount / 100))
        return new_price.quantize(Decimal('0'))

    def __str__(self):
        return self.name

    def average_rating(self):
        comments = self.comments.all()
        if comments.exists():
            return sum(comment.rating for comment in comments) / comments.count()
        return 0

    class Meta:
        ordering = ['my_order']
        verbose_name = 'product'
        verbose_name_plural = 'products'


class Comment(BaseModel):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    rating = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.full_name} - {self.product.name} ({self.rating}⭐)"

    class Meta:
        ordering = ['-created_at']


class Order(BaseModel):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    order_id = models.CharField(max_length=20, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    billing_address = models.TextField(default="No Billing Address")
    shipping_address = models.TextField(default="No Shipping Address")
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_totals(self):
        self.subtotal = sum(
            item.quantity * item.product.discounted_price for item in self.order_items.all()
        )
        self.tax = (self.subtotal * Decimal(0.05)).quantize(Decimal('0.01'))
        self.total = self.subtotal + self.tax
        self.save()

    def __str__(self):
        return f"Order #{self.order_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


def generate_invoice_prefix():
    return ''.join(random.choices(string.ascii_uppercase, k=5))


class Customer(BaseModel):
    full_name = models.CharField(max_length=255, default="No Name")
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True, null=True, default="No Description")
    vat_number = models.CharField(max_length=50, blank=True, null=True, default="No VAT number")
    customer_image = models.ImageField(upload_to='customers/img', default='customers/default_avatar.png')
    send_email_to = models.EmailField()
    address = models.TextField()
    phone_number = PhoneNumberField(region="UZ")
    invoice_prefix = models.CharField(max_length=5, default=generate_invoice_prefix, unique=True)
    invoice_number = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.invoice_prefix:
            self.invoice_prefix = generate_invoice_prefix()
        if self.invoice_number is None:
            self.invoice_number = 1
        super().save(*args, **kwargs)

    def generate_invoice_id(self):
        return f"{self.invoice_prefix}-{self.invoice_number:05d}"

    def __str__(self):
        return f'{self.full_name} -> {self.generate_invoice_id()}'

    @staticmethod
    def get_admin_email():
        return "admin@example.com"


class ShoppingCart(BaseModel):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='shopping_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shopping_cart')

    def get_total_price(self):
        return self.product.discounted_price

    def __str__(self):
        return f'{self.user} -> {self.product}'


# New model for Product Images
class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_images/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        verbose_name = 'product image'
        verbose_name_plural = 'product images'


# Signal for handling product-related actions
@receiver(pre_save, sender=Comment)
def before_save_comment(sender, instance, **kwargs):
    if instance.rating < 1 or instance.rating > 5:
        raise ValueError("Rating must be between 1 and 5")

@receiver(post_save, sender=Comment)
def after_save_comment(sender, instance, created, **kwargs):
    print(f"New comment added for product {instance.product.name}: {instance.rating}⭐")

    # Admin emailini bazadan olish
    admin_email = Customer.get_admin_email()

    if admin_email:
        send_mail(
            'New Comment Added',
            f"A new comment has been added for the product {instance.product.name} with a rating of {instance.rating}⭐.",
            'muzaffaribrohimov7777@gmail.com',
            [admin_email],
            fail_silently=False,
        )

@receiver(pre_delete, sender=Product)
def before_delete_product(sender, instance, **kwargs):
    print(f"Deleting product: {instance.name}")

@receiver(post_delete, sender=Product)
def after_delete_product(sender, instance, **kwargs):
    print(f"Product deleted: {instance.name}")

@receiver(pre_save, sender=Customer)
def before_save_customer(sender, instance, **kwargs):
    if not instance.invoice_prefix:
        instance.invoice_prefix = generate_invoice_prefix()

@receiver(post_save, sender=Product)
def after_save_product(sender, instance, created, **kwargs):
    if created:
        print(f"New product added: {instance.name}")
    else:
        print(f"Product updated: {instance.name}")

@receiver(post_save, sender=OrderItem)
def update_order_totals(sender, instance, created, **kwargs):
    order = instance.order
    order.calculate_totals()

@receiver(post_save, sender=Order)
def after_save_order(sender, instance, created, **kwargs):
    if created:
        print(f"New order created: {instance.order_id}")
        instance.calculate_totals()
