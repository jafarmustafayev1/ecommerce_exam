from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm
from django.core.mail import send_mail
from user.forms import LoginForm
from config.settings import DEFAULT_FROM_EMAIL
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model

User = get_user_model()  # Custom User modelini olish



# Create your views here.


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('ecommerce:index')
            else:
                messages.add_message(request,
                                     messages.ERROR,
                                     'Invalid login')
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context=context)


def logout_page(request):
    logout(request)
    return redirect('ecommerce:index')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.is_staff = True
            user.is_superuser = True
            user.save()

            verification_code = get_random_string(4, '0123456789')
            request.session['verification_code'] = verification_code  # Sessiyada saqlash
            request.session['email'] = user.email

            send_mail(
                "Ro‘yxatdan o'tish tasdiqlash kodi",
                f"Sizning tasdiqlash kodingiz: {verification_code}",
                DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
            return redirect("user:verify")
        else:
            messages.error(request, "Registration failed. Please check your input.")
    else:
        form = RegisterForm()

    return render(request, "user/register.html", {"form": form})

def verify_email(request):
    if request.method == "POST":
        entered_code = request.POST.get("code")
        verification_code = request.session.get("verification_code")
        email = request.session.get("email")

        if not verification_code or not email:
            messages.error(request, "Tasdiqlash kodi topilmadi.")
            return redirect("user:register")

        if entered_code == verification_code:
            try:
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()

                del request.session["verification_code"]
                del request.session["email"]

                login(request, user)
                return redirect("ecommerce:index")
            except User.DoesNotExist:
                messages.error(request, "Foydalanuvchi topilmadi!")
                return redirect("user:register")
        else:
            messages.error(request, "Kod noto‘g‘ri!")
            return redirect("user:verify")

    return render(request, "user/verify.html")