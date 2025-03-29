from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


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


class ReviewForm(forms.Form):
    text_review = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Ваша рецензія", "minlength": "25", "maxlength": "3000"}))
    rating = forms.IntegerField(min_value=1, max_value=10, required=True, widget=forms.HiddenInput())

    # this method removes '\r' because some browsers or operating systems may add it
    # this can cause issues with length validation on both the frontend and backend
    def clean_text_review(self):
        text_review = self.cleaned_data["text_review"].replace("\r", "")
        if len(text_review) > 3000:
            raise ValidationError(_("Review can not be longer than 3000 symbols."))
        if len(text_review) < 25:
            raise ValidationError(_("Review can not be smaller than 25 symbols."))

        return text_review