from django.contrib import admin
from django.urls import path
from ecommerce import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail')
]
