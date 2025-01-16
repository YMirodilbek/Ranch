from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import CustomUser  # Agar sizda CustomUser modeli bo'lsa
from django.core.validators import RegexValidator
from .models import *
class CustomUserForm(forms.ModelForm):
    # Telefon raqami uchun validatsiya
    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak."
    ) 
    
    # Parol va parolni tasdiqlash uchun
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol kamida 8 ta simvol'}),
        label='Parol'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parolni tasdiqlash'}),
        label='Parolni tasdiqlash'
    )

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name', 'phone_number', 'username']  # foydalanuvchi nomi 'username' modelga bog'liq
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiya ism sharifini kiriting'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon raqam kiriting'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Yangi login kiriting'}),
            
        }
    # Parollarni tasdiqlash
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Parollar mos kelmaydi.")
        return cleaned_data



from django.contrib.auth.forms import AuthenticationForm

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )



class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Telefon raqamingiz', 'class': 'form-control'}),
        label="Telefon raqami"
    )


class VerificationCodeForm(forms.Form):
    code = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={'placeholder': 'Tasdiqlash kodini kiriting', 'class': 'form-control'}),
        label="Tasdiqlash kodi"
    )



class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Yangi parol', 'class': 'form-control'}),
        label="Yangi parol"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Parolni takrorlang', 'class': 'form-control'}),
        label="Parolni takrorlang"
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError("Parollar mos emas.")
        return cleaned_data












class SearchForm(forms.Form):
    query = forms.CharField(
        label='Qidiruv',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Qidiruvni kiriting...',
            'class': 'search',
        })
    )

