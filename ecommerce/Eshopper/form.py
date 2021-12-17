from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, models, widgets
from Eshopper.models import User
from django import forms


class MyUserCreationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control required','placeholder':'Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control required','placeholder':'Confirm-Password'}))
    class Meta:
        model = User
        fields=['username','first_name','last_name','email','password1','password2']
    
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-control required','placeholder':'username'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control required','placeholder':'Email'}),
            'first_name' : forms.TextInput(attrs={'class': 'form-control required','placeholder':'First Name'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control required','placeholder':'Last Name'}),
            'password1' : forms.PasswordInput(attrs={'class': 'form-control required','placeholder':'Password'}),
            'password2' : forms.PasswordInput(attrs={'class': 'form-control required','placeholder':'Confirm-Password'}),
        }
    
class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password']

        widgets={
            'username' : forms.TextInput(attrs={'class': 'form-control required','placeholder':'username'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control required','placeholder':'Password'}),

        }


