from django.urls import path

from userpage.views import home


urlpatterns = [
    path('',home),
]