import json
import threading
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout

from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import account_activation_token
from django.utils.encoding import force_bytes,force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.views.generic import View
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from validate_email import validate_email


class EmailThreading(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send(fail_silently = False)


class RegistrationView(View):
    def get(self, request):
        return render(request, 'auth/register.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context={
            'fieldValues':request.POST
        }

        if not User.objects.filter(username = username).exists():
            if not User.objects.filter(email = email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password should be at least 6 characters long')
                    return render(request, 'auth/register.html',context)
                
                user = User.objects.create_user(username = username,email = email)
                user.set_password(password)
                user.is_active = False
                user.save()


                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
              

               
                link = reverse('activate',kwargs = {"uidb64":email_body['uid'],"token":email_body['token']})
                
                email_subject = "Activate Your Account"
                activate_url = 'http://'+ current_site.domain + link
                
                email = EmailMessage(
                    email_subject,
                    'Hi ' + user.username + 'Please use this link to verify your Account\n' + activate_url,
                    "noreply@semicolon.com",
                    [email],
                   
                )
                EmailThreading(email).start()
                messages.success(request, 'Account created Successfully.')
                return render(request, 'auth/register.html')

        return render(request, 'auth/register.html')
    


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'email is Invalid'},status=400)
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error': 'email already exists. Choose another User.', 'available': True},status=400)
        return JsonResponse({'email_valid':True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric charaters', 'available': True},status=400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error': 'username already exists. Choose another User.', 'available': True},status=400)
        return JsonResponse({'username_valid':True})
    

class VerificationView(View):
    def get(self, request,uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated Successfully.')
            return redirect('login')


        except Exception as ex:
            pass
        return redirect('login')
    



class LoginView(View):
    def get(self, request):
        # If user is already logged in, redirect to the role selection page
        if request.user.is_authenticated:
            return redirect('role_selection')  # Redirect to role selection view

        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username')  # Use get() to avoid KeyError
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome, {user.username}! You are logged in.')
                    return redirect('role_selection')  # Redirect to the role selection page
                else:
                    messages.error(request, 'Account is not active. Please check your email.')
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
        else:
            messages.error(request, 'Please fill in both username and password.')

        return render(request, 'auth/login.html')


class LogoutView(View):
    def post(self,request):
        logout(request)
        messages.success(request,"You have been logged Out.")
        return redirect('login')  # Redirect to login page or any other page

