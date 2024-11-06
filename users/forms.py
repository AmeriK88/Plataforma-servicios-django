# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    is_company = forms.BooleanField(required=False, label="¿Eres una compañía?")
    is_client = forms.BooleanField(required=False, label="¿Eres un cliente?")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_company', 'is_client', 'password1', 'password2')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'address']  