from django.urls import path


from giveAway.views import LandingPage, AddDonation, LoginView, RegisterView, Logout, ConfirmationView, UserView, \
    UserDetailView

urlpatterns = [
    path('', LandingPage.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('donate/', AddDonation.as_view(), name='donate'),
    path('donate/confirmation/', ConfirmationView.as_view(), name='confirmation'),
    path('user/', UserView.as_view(), name='user'),
    path('user/<int:donation_id>/', UserDetailView.as_view(), name='user-detail'),

]