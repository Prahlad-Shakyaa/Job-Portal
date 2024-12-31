from django.shortcuts import render
from jobs.models import JobPost
from profilee.models import JobSeeker
from profilee.models import Employer

def homepage(request):
    # Fetch the latest 3 job posts
    jobs = JobPost.objects.order_by('-created_at')[:3]

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

def contact_page(request):
    return render(request, 'design/contact.html')
