from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    is_seller = forms.BooleanField(required=False, label="Register as Seller")
    is_buyer = forms.BooleanField(required=False, label="Register as Buyer")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_seller', 'is_buyer', 'password1', 'password2']
