from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('register/',RegistrationView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),

    path('authentication/validate-username',csrf_exempt(UsernameValidationView.as_view()),name='validate-username'),
    path('authentication/validate-email',csrf_exempt(EmailValidationView.as_view()),name='validate-email'),
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name='activate'),

]
