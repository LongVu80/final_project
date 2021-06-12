from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, fields
from django.contrib.auth.models import User
from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('title', 'image')


class UserRegistrationForm(UserCreationForm):
    firstName = forms.CharField(max_length=101)
    lastName = forms.CharField(max_length=101)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'firstName', 'lastName', 'email', 'password1', 'password2']