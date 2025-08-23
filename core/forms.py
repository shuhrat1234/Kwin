from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    class Meta:
        model = User
        fields = ["username", "phone", "password"]
        labels = {
            "username": "Имя и фамилия",
            "phone": "Телефон",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        phone = cleaned_data.get("phone")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        if phone and User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Этот номер телефона уже зарегистрирован")
        return cleaned_data

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Телефон", max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Телефон (+998XXXXXXXXX)', 'pattern': '\+998[0-9]{9}'}))
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        fields = ["username", "password"]