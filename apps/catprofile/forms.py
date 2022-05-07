from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import CatProfile

class CatProfileForm(forms.ModelForm):
    class Meta:
        model = CatProfile
        fields = ('avatar','email',)

class SignUpForm(UserCreationForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'avatar']