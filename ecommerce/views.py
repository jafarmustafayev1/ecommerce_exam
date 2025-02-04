from django.shortcuts import render, get_object_or_404

from ecommerce.models import Product, Specification, ProductAttribute


# Create your views here.
def index(request):
    products = Product.objects.all()
    product_attributes = ProductAttribute.objects.filter()
    context = {
        'products': products
    }
    return render(request,'ecommerce/product-list.html',context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request,'ecommerce/product-details.html',context)
