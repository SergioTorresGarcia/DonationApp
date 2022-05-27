from django.urls import path


from giveAway.views import (
    LandingPage,
    RegisterView,
    LoginView,
    Logout,

    AddDonation,
    ConfirmationView,
    UserView,
    UserDetailView,
    # UpdateProfileView,
)

app_name = 'giveAway'
urlpatterns = [
    path('', LandingPage.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('donate/', AddDonation.as_view(), name='donate'),
    path('donate/confirmation/', ConfirmationView.as_view(), name='confirmation'),
    path('user/', UserView.as_view(), name='user'),
    path('user/<int:donation_id>/', UserDetailView.as_view(), name='user-detail'),
    # path('user/edit/<int:pk>/', UpdateProfileView.as_view(), name='edit_user'),
]
