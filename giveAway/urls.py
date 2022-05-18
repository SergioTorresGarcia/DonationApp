from django.urls import path


from giveAway.views import LandingPage, AddDonation, LoginView, RegisterView, Logout

urlpatterns = [
    path('', LandingPage.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('donate/', AddDonation.as_view(), name='donate'),

]