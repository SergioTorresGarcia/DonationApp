from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import Account, Donation


class UserAdminCreationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """
    class Meta:
        model = get_user_model()
        fields = ['email']


class LoginForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email '})
        }


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = ['user']
        widgets = {
            'pick_up_date': forms.SelectDateWidget()
        }

