from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),  # URL for the homepage
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_us, name='contact_us'),
    path('thank-you/', views.thank_you, name='thank_you'),
]
