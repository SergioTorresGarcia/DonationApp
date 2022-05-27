from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import Account, Donation


class UserAdminCreationForm(UserCreationForm):
    """ A Custom form for creating new users """
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


# class UpdateProfile(forms.ModelForm):
#     email = forms.EmailField(required=True)
#     first_name = forms.CharField(required=False)
#     last_name = forms.CharField(required=False)
#
#     class Meta:
#         model = Account
#         fields = ('email', 'first_name', 'last_name')
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#
#         if email.count():
#             raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
#         return email
#
#     def save(self, commit=True):
#         user = super(RegisterForm, self).save(commit=False)
#         user.email = self.cleaned_data['email']
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#
#         if commit:
#             user.save()
#
#         return user

