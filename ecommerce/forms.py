from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from ecommerce.models import *


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['full_name', 'email', 'body', 'rating']

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'email','description','vat_number', 'address', 'phone_number']
