from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name="login_page"),
    path('logout/', views.logout_page, name='logout_page'),
]
