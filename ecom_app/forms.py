from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter Your UserName'
            }
        ))
    email=forms.EmailField(widget=forms.EmailInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter Your Email'
            }
        ))
    password1=forms.CharField(widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Enter Your Password'
            }
        ))
    password2=forms.CharField(widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'placeholder':'Re-Enter Your Password'
            }
        ))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
