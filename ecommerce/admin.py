from django.contrib import admin
from ecommerce.models import Product, Category, Img , Specification
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Img)
admin.site.register(Specification)
