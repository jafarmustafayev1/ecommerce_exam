from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from adminsortable2.admin import SortableAdminMixin
from django.utils.html import format_html

# **Barcha modellarni models.py dan import qilish**
from .models import (
    Category, Product, Image, Comment, Order, OrderItem,
    Customer, ShoppingCart, Attribute, AttributeValue, ProductAttribute
)

admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin Portal"
admin.site.index_title = "Welcome to Ecommerce Researcher Portal"


@admin.register(Product)
class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'my_order')
    search_fields = ('name', 'price')
    list_filter = ('category', 'quantity')
    autocomplete_fields = ['category']


class ProductInline(admin.TabularInline):
    model = Product


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'product_count')
    search_fields = ('title',)
    inlines = [ProductInline]

    def product_count(self, category):
        return category.products.count()


# **Barcha modellarni ro‘yxatga olish**
admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)
admin.site.register(Comment)
admin.site.register(ShoppingCart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
