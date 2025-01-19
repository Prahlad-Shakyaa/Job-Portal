from jobs.models import JobPost
from profilee.models import JobSeeker
from profilee.models import Employer
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail


def homepage(request):
    # Fetch the latest 3 job posts
    jobs = JobPost.objects.order_by('-created_at')[:4]

    # Determine user roles
    job_seeker = False
    employer = False
    if request.user.is_authenticated:
        job_seeker = JobSeeker.objects.filter(user=request.user).exists()
        employer = Employer.objects.filter(user=request.user).exists()

    # Pass user role information along with job posts to the template
    context = {
        'jobs': jobs,
        'job_seeker': job_seeker,
        'employer': employer,
    }

    return render(request, 'design/homepage/index.html', context)



def about_page(request):
    return render(request, 'design/about.html')

# def contact_page(request):
#     return render(request, 'design/contact.html')



def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()

            # Send an email
            subject = f"New Contact Us Message from {form.cleaned_data['name']}"
            message = f"Message from: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\n\n{form.cleaned_data['message']}"
            from_email = form.cleaned_data['email']
            recipient_list = ['prahladshakya2058@gmail.com']  # The recipient email address

            # Send the email
            send_mail(subject, message, from_email, recipient_list)

            # Redirect to a "Thank You" page or the same page
            return redirect('thank_you')  # Adjust the redirect as needed
    else:
        form = ContactForm()

    return render(request, 'design/contact_us.html', {'form': form})

def thank_you(request):
    return render(request, 'design/thank_you.html')


