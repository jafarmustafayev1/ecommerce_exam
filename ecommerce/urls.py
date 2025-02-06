from django.urls import path
from ecommerce import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/', views.customer_details, name='customer_detail'),
    path('customer-create/', views.customer_create, name='customer_create'),
    path('customer-edit/<int:pk>/', views.customer_edit, name='customer_edit'),
]

