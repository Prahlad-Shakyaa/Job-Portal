from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),  # URL for the homepage
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
]
