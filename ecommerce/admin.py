from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from adminsortable2.admin import SortableAdminMixin

# Import all models from models.py
from .models import (
    Category, Product, ProductImage, Comment, Order, OrderItem,
    Customer, ShoppingCart
)

admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin Portal"
admin.site.index_title = "Welcome to Ecommerce Admin Portal"


# @admin.register(Product) ni olib tashlash kerak, chunki 'ProductInline'ni ishlatishning hojati yo'q
@admin.register(Product)
class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'stock', 'favorite', 'discounted_price')
    search_fields = ('name', 'price')
    list_filter = ('category', 'stock', 'favorite')
    autocomplete_fields = ['category']  # Bu mavjud
    # prepopulated_fields = {"slug": ("name",)}  # Bu o'chirildi, chunki slug maydoni yo'q

    def discounted_price(self, obj):
        return obj.discounted_price
    discounted_price.admin_order_field = 'discounted_price'  # Allows ordering by discounted price
    discounted_price.short_description = 'Discounted Price'


@admin.register(Category)
class CategoryModelAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'created_at', 'product_count', 'my_order')
    search_fields = ('title',)

    def product_count(self, category):
        return category.products.count()

    product_count.admin_order_field = 'product_count'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('full_name', 'product__name', 'email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'status', 'email', 'total', 'date')
    list_filter = ('status', 'date')
    search_fields = ('order_id', 'email', 'phone')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('order__order_id', 'product__name')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'generate_invoice_id', 'created_at')
    search_fields = ('full_name', 'email')
    readonly_fields = ('generate_invoice_id',)

    def generate_invoice_id(self, obj):
        return obj.generate_invoice_id()

    generate_invoice_id.admin_order_field = 'invoice_prefix'
    generate_invoice_id.short_description = 'Invoice ID'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'get_total_price')
    search_fields = ('user__full_name', 'product__name')

    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.admin_order_field = 'get_total_price'  # Sorting by total price


# Register ProductImage model for managing product images
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_primary')
    list_filter = ('is_primary',)
    search_fields = ('product__name',)
