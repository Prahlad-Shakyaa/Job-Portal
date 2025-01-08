from jobs.models import JobPost
from profilee.models import JobSeeker
from profilee.models import Employer
from django.shortcuts import render, redirect
from .forms import ContactForm

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
            form.save()  # Save the form data to the database
            return redirect('thank_you')  # Redirect to a "Thank You" page or the same page
    else:
        form = ContactForm()

    return render(request, 'design/contact_us.html', {'form': form})

def thank_you(request):
    return render(request, 'design/thank_you.html')


