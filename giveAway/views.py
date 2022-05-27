from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

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
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            user.set_password(password)
            user.set_password(password2)
            if password == password2:
                user.save()
                return redirect('login')
        error = "Hasła się nie zgadzają"
        return render(request, 'register.html', {'form': form, 'error': error})


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
        error = "Podany login lub hasło jest nieprawidłowe!"
        return render(request, 'registration/login.html', {'form': form, 'error': error})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class LandingPage(View):
    """
    Displays home page:
        - total of donations
        - nr. of institutions that have recieved donations
        - all info about the app
    """
    def get(self, request):
        all_donations = Donation.objects.all()
        total_bags_given = sum(all_donations.values_list('quantity', flat=True))
        nr_inst_helped = Donation.objects.aggregate(Count('institution',distinct=True)).get('institution__count')
        all_institutions = Institution.objects.all()
        ctx = {
            'total_bags_given': total_bags_given,
            'nr_inst_helped': nr_inst_helped,
            'all_institutions': all_institutions
        }
        return render(request, 'index.html', ctx)


class AddDonation(View):
    """ Displays form to guide user through the process (4x JS slides) """
    def get(self, request):
        all_categories = Category.objects.all()
        all_institutions = Institution.objects.all()
        return render(request, 'form.html', {
            'all_categories': all_categories,
            'all_institutions': all_institutions,
        })

    def post(self, request):
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()
            form.save_m2m()
            return JsonResponse({'url': reverse('giveAway:confirmation')})  # we get response from JS not django!
        return JsonResponse({'url': reverse('giveAway:donate')})


class ConfirmationView(View):
    def get(self, request):
        user = request.user
        return render(request, 'form-confirmation.html', {'user': user})


class UserView(View):
    def get(self, request):
        user = request.user
        user_donations = Donation.objects.filter(user=user)
        return render(request, 'user.html', {'user_donations': user_donations})


# class UpdateProfileView(View):
#     def get(self, request, user_id):
#         args = {}
#
#         if request.method == 'POST':
#             actual_user = Account.objects.get(pk=user_id)
#             form = UpdateProfile(request.POST, instance=request.user)
#             form.actual_user = request.user
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect(reverse('user'))
#         else:
#             form = UpdateProfile()
#
#         args['form'] = form
#         return render(request, 'register.html', args)


# class EditUserView(View):
#     def get(self, request, user_id):
#         form = UpdateProfile(RegisterForm)
#         user = request.user
#         user_donations = Donation.objects.filter(user=user)
#         user_to_update = Account.objects.get(pk=user_id)
#         # user_to_update.is_taken = True
#         # user_to_update.save()
#         return render(request, 'user.html', {'user_donations': user_donations })
#
#     def post(self, request):
#         user = request.user
#         user_donations = Donation.objects.filter(user=user)
#         return render(request, 'user.html', {'user_donations': user_donations})


class UserDetailView(View):
    def get(self, request, donation_id):
        user = request.user
        user_donations = Donation.objects.filter(user=user)
        donation_to_update = Donation.objects.get(pk=donation_id)
        donation_to_update.is_taken = True
        donation_to_update.save()
        return render(request, 'user.html', {
            'donation_to_update': donation_to_update,
            'user_donations': user_donations
        })


@method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'form.html'
