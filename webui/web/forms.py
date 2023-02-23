from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import USER
from django.utils import timezone

class RegisterForm(UserCreationForm):
    # username = forms.CharField(label="username", max_length=20)
    # email_address = forms.CharField(label="email_address", max_length=50)
    # password = forms.CharField(label="password", max_length=20)
    # reconfirm_password = forms.CharField(label="reconfirm_password", max_length=20)
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2"
        ]

class CustomRegisterForm(forms.ModelForm):
    password2 = forms.CharField()
    class Meta:
        model = USER
        fields = (
            'username',
            'email',
            'password1'
        )

# class ImageForm(forms.ModelForm):
#     # image = forms.ImageField(widget=forms.ImageField(attrs={'onchange': 'submit();'}))
#     class Meta:
#         model = Image
#         fields = ['image']

class ImageForm(forms.Form):
    image = forms.ImageField()