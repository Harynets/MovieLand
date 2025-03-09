from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Ім'я користувача:", widget=forms.TextInput(
        attrs={"placeholder": "Ім'я користувача", "class": "form-control"}))
    email = forms.EmailField(label="Email адреса:", required=True, widget=forms.TextInput(
        attrs={"placeholder": "Email адреса", "class": "form-control"}))
    password1 = forms.CharField(label="Пароль:",
                                widget=forms.PasswordInput(attrs={"placeholder": "Пароль", "class": "form-control"}))
    password2 = forms.CharField(label="Підтвердження пароля:", widget=forms.PasswordInput(
        attrs={'placeholder': "Підтвердження пароля", "class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class AuthenticationUserForm(AuthenticationForm):
    username = forms.CharField(label="Ім'я користувача:", widget=forms.TextInput(
        attrs={"placeholder": "Ім'я користувача", "class": "form-control"}))
    password = forms.CharField(label="Пароль:",
                                widget=forms.PasswordInput(attrs={"placeholder": "Пароль", "class": "form-control"}))
