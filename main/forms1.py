from django import forms
from .models import CustomUser, Tarif, Group, Student, Tolov
from django.core.exceptions import ValidationError
import datetime

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'lavozim', 'birth_year']
        widgets = {
            'birth_year': forms.DateInput(attrs={'type': 'date'}),  # date picker widget
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 13:
            raise ValidationError("Telefon raqam 13 ta raqamdan iborat bo'lishi kerak!")
        return phone


class TarifForm(forms.ModelForm):
    class Meta:
        model = Tarif
        fields = ['name', 'price']
        


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'teacher', 'amount', 'start_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'birth_year', 'phone', 'group', 'is_paid']
        widgets = {
            'birth_year': forms.DateInput(attrs={'type': 'date'}),
            'is_paid':forms.BooleanField()
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 13:
            raise ValidationError("Telefon raqam 13 ta raqamdan iborat bo'lishi kerak!")
        return phone


class TolovForm(forms.ModelForm):
    class Meta:
        model = Tolov
        fields = ['amount', 'date', 'student_name', 'group']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
