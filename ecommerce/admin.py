from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from ecommerce.models import (
    Product, Category, Img, Specification, Attribute, AttributeValue, ProductAttribute, Customer
)
from django.utils.html import format_html
from .forms import CustomerEditForm
from adminsortable2.admin import SortableAdminMixin

# Admin saytining o'zgarishlari
admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin Portal"
admin.site.index_title = "Welcome to Ecommerce Researcher Portal"


# Category modelining admin ko'rinishi
@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'product_count')
    search_fields = ('title',)
    inlines = []

    def product_count(self, category):
        return category.products.count()


# Product modelining admin ko'rinishi
@admin.register(Product)
class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'image_tag', 'my_order')
    search_fields = ('name', 'price')
    list_filter = ('category', 'quantity', 'rating', 'stock')
    autocomplete_fields = ['category']
    list_editable = ('my_order',)

    # Mahsulotning rasmiga tegishli tasvirni ko'rsatish
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:50px; max-height:50px"/>'.format(obj.image.url))
        return "No Image"

    image_tag.short_description = 'Image'


# Img modelining admin ko'rinishi
@admin.register(Img)
class ImgAdmin(admin.ModelAdmin):
    list_display = ('image', 'product', 'created_at')
    search_fields = ('product__name',)


# Specification modelining admin ko'rinishi
@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'created_at')
    search_fields = ('name',)


# Attribute modelining admin ko'rinishi
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# AttributeValue modelining admin ko'rinishi
@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('value',)
    search_fields = ('value',)


# ProductAttribute modelining admin ko'rinishi
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'attribute_value')
    search_fields = ('product__name', 'attribute__name', 'attribute_value__value')
    list_filter = ('attribute', 'attribute_value')


# Customer modelining admin ko'rinishi
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('created_at',)
    form = CustomerEditForm  # Use the custom form for editing customers

# Register Customer model using the custom admin (keep this line only)
admin.site.register(Customer, CustomerAdmin)
