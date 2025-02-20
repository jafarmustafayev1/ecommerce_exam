from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import JsonResponse
from ecommerce.utils import generate_invoice_prefix



from ecommerce.models import Product, Customer, ShoppingCart, Comment
from ecommerce.forms import CustomerModelForm


# def index(request):
    # search_query = request.GET.get('q', '')
    # filter_type = request.GET.get('filter', '')
    # products = Product.objects.all()
    #
    # if filter_type == 'date':
    #     products = Product.objects.all().order_by('-created_at')
    # elif filter_type == 'name':
    #     products = Product.objects.all().order_by('name')
    # elif filter_type == 'stock':
    #     products = Product.objects.all().order_by('-stock')
    # elif filter_type == 'price_rating':
    #     products = Product.objects.all().order_by('-price', '-rating')
    #
    # else:
    #     products = Product.objects.all()
    #
    # if search_query:
    #     products = Product.objects.filter(name__icontains=search_query)
    #
    # paginator = Paginator(products,4)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    #
    # context = {
    #     'page_obj': page_obj,
    #     'products': products,
    #     # 'cart_items': cart_items,
    # }
    # return render(request, 'ecommerce/product-list.html', context)


# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     comments = Comment.objects.filter(product=product)
#     context = {
#         'product': product,
#         'comments': comments
#     }
#     return render(request, 'ecommerce/product-details.html', context)
# --------------------------------------------------------------------

def index(request):
    search_query = request.GET.get('q', '')
    filter_type = request.GET.get('filter', '')
    products = Product.objects.all()

    if filter_type == 'date':
        products = products.order_by('-created_at')
    elif filter_type == 'name':
        products = products.order_by('name')
    elif filter_type == 'stock':
        products = products.order_by('-stock')
    elif filter_type == 'price_rating':
        products = products.order_by('-price', '-rating')

    if search_query:
        products = products.filter(name__icontains=search_query)

    # Har bir mahsulot uchun o'rtacha reyting qo'shish
    for product in products:
        product.average_rating = Comment.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'products': products,
    }
    return render(request, 'ecommerce/product-list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comments = Comment.objects.filter(product=product)

    # O'rtacha reytingni hisoblash
    average_rating = comments.aggregate(Avg('rating'))['rating__avg'] or 0
    product.average_rating = round(average_rating, 1)

    context = {
        'product': product,
        'comments': comments,
        'average_rating': product.average_rating,
    }
    return render(request, 'ecommerce/product-details.html', context=context)

# def comment_view(request, pk):
#     product = get_object_or_404(Product, id=pk)
#     if request.method == "POST":
#         full_name = request.POST.get("full_name")
#         email = request.POST.get("email")
#         body = request.POST.get("body")
#         rating = request.POST.get("rating") or 1
#
#         Comment.objects.create(
#             product=product,
#             full_name=full_name,
#             email=email,
#             body=body,
#             rating=int(rating)
#         )
#
#         # Yangi sharh qo'shilgandan keyin reytingni yangilash
#         new_avg_rating = Comment.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg'] or 0
#         product.average_rating = round(new_avg_rating, 1)
#         product.save(update_fields=['average_rating'])
#
#         messages.success(request, "Your review has been submitted successfully.")
#         return redirect("ecommerce:product_detail", pk=product.id)
#
#     return redirect("ecommerce:product_detail", pk=product.id)
#
# def order_list(request):
#     return render(request, 'ecommerce/order-list.html')

#---------------------------------------------------------------------------------------------------------------------

def comment_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    form  = CustomerModelForm()
    if request.method == "POST":
        form = CustomerModelForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('ecommerce:product-details', pk)

        else:
            print(form.errors)

    context = {
        'form': form,
        'product': product,
    }


    return render(request, "ecommerce/product-details.html", context=context)


# class CommentCreateView(View):
#     def post(self, request, pk):
#         product = get_object_or_404(Product, id=pk)
#         full_name = request.POST.get("full_name")
#         email = request.POST.get("email")
#         body = request.POST.get("body")
#         rating = request.POST.get("rating", 1)
#
#         Comment.objects.create(
#             product=product, full_name=full_name, email=email, body=body, rating=int(rating)
#         )
#         messages.success(request, "Your review has been submitted successfully.")
#         return redirect("ecommerce:product_detail", pk=product.id)


def customer_list(request):
    filter_type = request.GET.get('filter', '')
    search_query = request.GET.get('q', '')
    customers = Customer.objects.all()

    if filter_type == 'filter':
        customers = Customer.objects.all().order_by('full_name')
    else:
        customers = Customer.objects.all().order_by('-created_at')

    for customer in customers:
        customer.created_date = customer.created_at.strftime("%B %d, %Y")

    if search_query:
        customers = Customer.objects.filter(full_name__icontains=search_query)

    context = {
        'customers': customers,
    }

    return render(request, template_name='ecommerce/customers.html', context=context)

# class CustomerListView(ListView):
#     model = Customer
#     template_name = 'ecommerce/customers.html'
#     context_object_name = 'customers'
#
#     def get_queryset(self):
#         queryset = Customer.objects.all()
#         search_query = self.request.GET.get('q', '')
#         filter_type = self.request.GET.get('filter', '')
#
#         if filter_type == 'filter':
#             queryset = queryset.order_by('full_name')
#         else:
#             queryset = queryset.order_by('-created_at')
#
#         if search_query:
#             queryset = queryset.filter(full_name__icontains=search_query)
#
#         return queryset

def customer_details(request, pk):
    customer = get_object_or_404(Customer, id=pk)
    created_date = customer.created_at.strftime("%b %d, %I:%M %p")

    context = {
        'customer': customer,
        'created_date': created_date,
    }

    return render(request, template_name='ecommerce/customer-details.html', context=context)

# class CustomerDetailView(DetailView):
#     model = Customer
#     template_name = 'ecommerce/customer-details.html'
#     context_object_name = 'customer'


def add_customer(request):
    if request.method == "POST":
        form = CustomerModelForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.invoice_prefix = generate_invoice_prefix()
            customer.invoice_number = 1
            customer.save()
            return redirect('ecommerce:customer_list')
    else:
        form = CustomerModelForm()

    return render(request, 'ecommerce/add_customer.html', {'form': form})

# class CustomerCreateView(CreateView):
#     model = Customer
#     form_class = CustomerModelForm
#     template_name = 'ecommerce/add_customer.html'
#     success_url = reverse_lazy('ecommerce:customer_list')


def edit_customer(request, pk):
    customer = get_object_or_404(Customer, id=pk)

    if request.method == "POST":
        form = CustomerModelForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.save()
            return redirect('ecommerce:customer_list')
    else:
        form = CustomerModelForm(instance=customer)

    return render(request, 'ecommerce/edit_customer.html', {'form': form})



def delete_customer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        customer.delete()
        return redirect('ecommerce: customer_list')
    except Customer.DoesNotExist as e:
        print(e)




def toggle_favourite(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    product.favorite = not product.favorite
    product.save()

    return JsonResponse({"favorite": product.favorite})




def view_cart(request):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, email=request.user.email)
        cart_items = ShoppingCart.objects.filter(user=customer)

        total_price = sum(cart.get_total_price() for cart in cart_items)

        if not cart_items:
            cart_items = None
            total_price = 0

    else:
        cart_items = None
        total_price = 0

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'ecommerce/shopping-cart.html', context)

# class CartView(LoginRequiredMixin, View):
#     def get(self, request):
#         customer = get_object_or_404(Customer, email=request.user.email)
#         cart_items = ShoppingCart.objects.filter(user=customer)
#         total_price = sum(cart.get_total_price() for cart in cart_items) if cart_items else 0
#         return render(request, 'ecommerce/shopping-cart.html', {'cart_items': cart_items, 'total_price': total_price})



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(email=request.user.email,
                                                           defaults={'full_name': request.user.get_full_name()})

        if ShoppingCart.objects.filter(user=customer, product=product).exists():
            messages.warning(request, "Bu mahsulot allaqachon savatchaga qo‘shilgan!")
        else:
            ShoppingCart.objects.create(user=customer, product=product)
            messages.success(request, "Mahsulot savatchaga qo‘shildi!")

    return redirect('ecommerce:index')

# class AddToCartView(LoginRequiredMixin, View):
#     def post(self, request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         customer, _ = Customer.objects.get_or_create(email=request.user.email, defaults={'full_name': request.user.get_full_name()})
#         if ShoppingCart.objects.filter(user=customer, product=product).exists():
#             messages.warning(request, "Bu mahsulot allaqachon savatchaga qo‘shilgan!")
#         else:
#             ShoppingCart.objects.create(user=customer, product=product)
#             messages.success(request, "Mahsulot savatchaga qo‘shildi!")
#         return redirect('ecommerce:index')


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(email=request.user.email,
                                                           defaults={'full_name': request.user.get_full_name()})

        cart_item = ShoppingCart.objects.filter(user=customer, product=product).first()

        if cart_item:
            cart_item.delete()
            messages.success(request, "Mahsulot savatchadan o‘chirildi!")
        else:
            messages.warning(request, "Bu mahsulot savatchada topilmadi!")
    else:
        messages.warning(request, "Iltimos, avval tizimga kiring.")

    return redirect('ecommerce:shopping_cart')

# class RemoveFromCartView(LoginRequiredMixin, View):
#     def post(self, request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         customer = get_object_or_404(Customer, email=request.user.email)
#         cart_item = ShoppingCart.objects.filter(user=customer, product=product).first()
#         if cart_item:
#             cart_item.delete()
#             messages.success(request, "Mahsulot savatchadan o‘chirildi!")
#         else:
#             messages.warning(request, "Bu mahsulot savatchada topilmadi!")
#         return redirect('ecommerce:shopping_cart')

def order_list(request):
    return render(request, 'ecommerce/order-list.html')

# class OrderListView(View):
#     def get(self, request):
#         return render(request, 'ecommerce/order-list.html')

