from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobSeekerProfileForm, EmployerProfileForm
from .models import JobSeeker, Employer
from django.contrib import messages




from django.shortcuts import render, redirect

def role_selection(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='JobSeeker').exists():
            return redirect('job_seeker_dashboard')  # Replace with your actual URL name for the Job Seeker dashboard
        elif request.user.groups.filter(name='Employer').exists():
            return redirect('employer_dashboard')  # Replace with your actual URL name for the Employer dashboard
    return redirect('home')  # Fallback if the user is not authenticated or has no role



@login_required
def job_seeker_profile(request):
    job_seeker, created = JobSeeker.objects.get_or_create(user=request.user)
    return render(request, 'profile/job_seeker_profile.html', {'job_seeker': job_seeker})


# def edit_job_seeker_profile(request):
#     try:
#         # Try to get the JobSeeker profile linked to the logged-in user
#         job_seeker_profile = JobSeeker.objects.get(user=request.user)
#     except JobSeeker.DoesNotExist:
#         # If the JobSeeker profile doesn't exist, create a new one
#         job_seeker_profile = JobSeeker(user=request.user)
#         job_seeker_profile.save()

#     if request.method == 'POST':
#         form = JobSeekerProfileForm(request.POST, request.FILES, instance=job_seeker_profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your Job Seeker profile has been updated successfully!')
#             return redirect('job_seeker_profile')  # Redirect to the job seeker profile view
#     else:
#         form = JobSeekerProfileForm(instance=job_seeker_profile)

#     return render(request, 'profile/job_seeker_profile_edit.html', {'form': form})
@login_required
def edit_job_seeker_profile(request):
    try:
        # Try to get the JobSeeker profile linked to the logged-in user
        job_seeker_profile = JobSeeker.objects.get(user=request.user)
        print("Job Seeker profile found")
    except JobSeeker.DoesNotExist:
        # If the JobSeeker profile doesn't exist, create a new one
        job_seeker_profile = JobSeeker(user=request.user)
        job_seeker_profile.save()
        print("New Job Seeker profile created")

    if request.method == 'POST':
        print("Received POST request")
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=job_seeker_profile)
        if form.is_valid():
            print("Form is valid")
            form.save()
            messages.success(request, 'Your Job Seeker profile has been updated successfully!')
            return redirect('job_seeker_profile')  # Adjust to your profile page URL
        else:
            print("Form errors:", form.errors)  # Log form errors
    else:
        print("GET request - Rendering form")
        form = JobSeekerProfileForm(instance=job_seeker_profile)

    return render(request, 'profile/job_seeker_profile_edit.html', {'form': form})


@login_required
def employer_profile(request):
    employer, created = Employer.objects.get_or_create(user=request.user)
    return render(request, 'profile/employer_profile.html', {'employer': employer})

@login_required
def edit_employer_profile(request):
    try:
        # Try to get the Employer profile linked to the logged-in user
        employer_profile = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        # If the employer doesn't exist, create a new one (optional)
        employer_profile = Employer(user=request.user)
        employer_profile.save()

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, instance=employer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Employer profile has been updated successfully!')
            return redirect('employer_profile')  # Redirect to the employer profile view
    else:
        form = EmployerProfileForm(instance=employer_profile)

    return render(request, 'profile/employer_profile_edit.html', {'form': form})

