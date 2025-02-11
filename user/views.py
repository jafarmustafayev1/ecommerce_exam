from django.shortcuts import render

# Create your views here.

def login_page(request):
    render(request, 'user/login.html')