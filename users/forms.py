from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        labels = {'username':'用户名',"password":"密码"}