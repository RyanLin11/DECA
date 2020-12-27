from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'event']

class ChangeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-user','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-user','placeholder':'Password'}))
    """
    class Meta:
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control form-control-user', 'id':'exampleInputPassword','placeholder':'Password...'}),
            'password':forms.PasswordInput(attrs={'class':'form-control form-control-user'}),
        }
    """