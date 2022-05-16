from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View

from accounts.forms import UserAdminCreationForm
from accounts.models import Donation, Institution, CustomUser, Category


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        try:
            if password1 == password2:
                user = CustomUser.objects.create(first_name=name, last_name=surname, email=email, password=password1)
                login(request, user)
                redirect_url = request.GET.get('next', '/')
                return redirect(redirect_url)
            else:
                error = "Passwords don't match"
                return render(request, 'register.html', {'error': error})
        except MultiValueDictKeyError:
            error = "Something went wrong, try again"
            return render(request, 'register.html', {'error': error})


class Login(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(email=email, password=password)
            if user:
                login(request, user)
                redirect_url = request.GET.get('next', '/')
                return redirect(redirect_url)
        except Exception:
            error = "Email and password don't match"
            return render(request, 'registration/login.html', {'error':error})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class LandingPage(View):
    """
    Homepage view. Greets user and displays "before login" menu:
    """
    def get(self, request):
        all_donations = Donation.objects.all()
        all_institutions = Institution.objects.all()
        total_bags_given = 0
        institutions_helped = []
        nr_inst_helped = 0
        for donation in all_donations:
            total_bags_given += int(donation.quantity)
            if donation.institution_id not in institutions_helped:
                institutions_helped.append(donation.institution_id)
                nr_inst_helped += 1
        ctx = {
            'total_bags_given': total_bags_given,
            'nr_inst_helped': nr_inst_helped,
            'all_institutions': all_institutions,
        }
        return render(request, 'index.html', ctx)


class AddDonation(View):
    """
    Displays form to guide user through the process (4x JS slides)
    """
    def get(self, request):
        all_categories = Category.objects.all()
        all_institutions = Institution.objects.all()
        return render(request, 'form.html', {
            'all_categories': all_categories,
            'all_institutions': all_institutions
        })