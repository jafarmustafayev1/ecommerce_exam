from django import forms
from .models import Customer

# Customer Create Form
class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']


    # Agar kerak bo'lsa, qo'shimcha validerlar qo'shishingiz mumkin
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu email manzili allaqachon ro\'yxatdan o\'tgan.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Bu telefon raqami allaqachon ro\'yxatdan o\'tgan.')
        return phone

# Customer Edit Form
class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']