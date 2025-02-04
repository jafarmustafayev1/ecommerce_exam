from email.headerregistry import Group

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from ecommerce.models import Product, Category, Img, Specification, Attribute, AttributeValue, ProductAttribute
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin

# admin.site.register(Product)
# admin.site.register(Category)
admin.site.register(Img)
admin.site.register(Specification)

admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin Portal"
admin.site.index_title = "Welcome to Ecommerce Researcher Portal"


@admin.register(Product)

class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'image_tag','my_order')
    search_fields = ('name', 'price')
    list_filter = ('category', 'quantity', 'rating' )
    autocomplete_fields = ['category']

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:50px; max-height:50px"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'

class ProductInline(admin.TabularInline):
    model = Product

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'product_count')
    search_fields = ('title',)

    inlines = [
        ProductInline,
    ]

    def product_count(self, category):
        return category.products.count()



admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)