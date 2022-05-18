from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.views import View

from accounts.forms import LoginForm, RegisterForm
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
        all_donations = Donation.objects.all()
        all_institutions = Institution.objects.all()
        current_donation = all_donations[0]

        return render(request, 'form.html', {
            'all_categories': all_categories,
            'all_institutions': all_institutions,
            'all_donations': all_donations,

        })

    def post(self, request):  # forms.py (validacja)
        Donation.objects.create(
            quantity = request.POST['bags'],
            # category = request.POST['categories'], < M2M - osobno
            # address = request.POST['address'],
            phone_number = request.POST['phone'],
            city = request.POST['city'],
            zip_code = request.POST['postcode'],
            pick_up_date = request.POST['date'],
            pick_up_time = request.POST['time'],
            pick_up_comment = request.POST['more_info'],
            institution = request.POST['organization'],
            user = request.user
        )
        return render(request, 'form-confirmation.html')

