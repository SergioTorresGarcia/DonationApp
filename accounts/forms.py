from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import Account, Institution, Donation


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
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password']
        labels = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': '',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email '})
        }


# class DonationForm(forms.Form):
#     quantity = forms.IntegerField()
#     # categories = forms.MultipleChoiceField('Category', widget=forms.CheckboxSelectMultiple),
#     institution = forms.ModelChoiceField(queryset=Institution.objects.all())
#     phone_number = forms.CharField(max_length=20)
#     address = forms.CharField(max_length=20)
#     city = forms.CharField(max_length=20)
#     zip_code = forms.IntegerField()
#     pick_up_date = forms.DateField() #initial=datetime.date
#     pick_up_time = forms.TimeField() #default=timezone.now
#     pick_up_comment = forms.CharField(widget=forms.Textarea) #default='Brak uwag'
#     user = forms.ModelChoiceField(queryset=Account.objects.all())
#     is_taken = forms.BooleanField()

class DonationModelForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = ['user', 'categories']
        widgets = {
            'pick_up_date': forms.SelectDateWidget()
        }