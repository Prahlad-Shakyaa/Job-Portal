from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobSeekerProfileForm, EmployerProfileForm
from .models import JobSeeker, Employer
from django.contrib import messages




def role_selection(request):
    if request.method == 'POST':
        selected_role = request.POST.get('role')
        if selected_role == 'job_seeker':
            return redirect('job_seeker_profile')  # Redirect to job seeker profile
        elif selected_role == 'employer':
            return redirect('employer_profile')  # Redirect to employer profile
    return render(request, 'profile/role_selection.html')


@login_required
def job_seeker_profile(request):
    job_seeker, created = JobSeeker.objects.get_or_create(user=request.user)
    return render(request, 'profile/job_seeker_profile.html', {'job_seeker': job_seeker})


@login_required
def edit_job_seeker_profile(request):
    profile, created = JobSeeker.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Job Seeker profile has been updated successfully!')
            return redirect('job_seeker_profile')  # Adjust to your profile page URL
    else:
        form = JobSeekerProfileForm(instance=profile)

    return render(request, 'profile/job_seeker_profile_edit.html', {'form': form})

@login_required
def employer_profile(request):
    employer, created = Employer.objects.get(user=request.user)
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

