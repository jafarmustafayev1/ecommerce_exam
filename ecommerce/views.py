from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Customer, Category
from ecommerce.models import Product
from .forms import CustomerEditForm , CustomerCreateForm

# Bosh sahifa - barcha mahsulotlar ro'yxati
def index(request):
    search_query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')

    if filter_type == 'date':
        products = Product.objects.all().order_by('-created_at')
    elif filter_type == 'name':
        products = Product.objects.all().order_by('name')
    elif filter_type == 'stock':
        products = Product.objects.all().order_by('-stock')
    elif filter_type == 'price_rating':
        products = Product.objects.all().order_by('-price', '-rating')

    else:
        products = Product.objects.all()

    if search_query:
        products = Product.objects.filter(name__icontains=search_query)

    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'ecommerce/product-list.html', context)



# Mahsulot tafsilotlari sahifasi
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'ecommerce/product-details.html', context)

# Mijozlar ro'yxatini ko'rsatish
def customer_list(request):
    customers = Customer.objects.all()  # Barcha mijozlarni olish
    return render(request, 'ecommerce/customers.html', {'customers': customers})

# Mijoz tafsilotlari sahifasi
def customer_details(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'ecommerce/customer-details.html', {'customer': customer})

# Yangi mijoz qo'shish
def customer_create(request):
    if request.method == 'POST':
        form = CustomerCreateForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('shop:customer_list')
    else:
        form = CustomerCreateForm()

    return render(request, 'ecommerce/customer-create.html', {'form': form})


# Edit customer view
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerEditForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()  # Save the updated customer
            return redirect('shop:customer_list', pk=customer.pk)  # Redirect to the customer's detail page
    else:
        form = CustomerEditForm(instance=customer)

    return render(request, 'ecommerce/customer-edit.html', {'form': form, 'customer': customer})
