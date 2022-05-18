from collections import Counter

from django.contrib.auth import logout, login, authenticate
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import LoginForm, RegisterForm, DonationForm
from accounts.models import Donation, Institution, Category


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                redirect_url = request.GET.get('next', '/')
                return redirect(redirect_url)
        error = "Podany login lub hasło jest nieprawidłowe !"
        return render(request, 'registration/login.html', {'form': form, 'error': error})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class LandingPage(View):
    def get(self, request):
        all_donations = Donation.objects.all()
        total_bags_given = sum(all_donations.values_list('quantity', flat=True))
        nr_inst_helped = Donation.objects.aggregate(Count('institution',distinct=True)).get('institution__count')

        ctx = {
            'total_bags_given': total_bags_given,
            'nr_inst_helped': nr_inst_helped,
        }
        return render(request, 'index.html', ctx)


class AddDonation(View):
    """
    Displays form to guide user through the process (4x JS slides)
    """
    def get(self, request):
        form = DonationForm()
        all_categories = Category.objects.all()
        all_institutions = Institution.objects.all()
        return render(request, 'form.html', {
            'form': form,
            'all_categories': all_categories,
            'all_institutions': all_institutions,
        })

    def post(self, request):
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save() #commit=False)
            donation.set_category(form.cleaned_data['categories']), #< M2M - osobno
            donation.save()
            return render(request, 'form-confirmation.html')
        return render(request, 'form.html', {'form': form})

