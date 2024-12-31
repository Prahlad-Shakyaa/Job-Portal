from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from profilee.models import Employer, JobSeeker
from .models import JobApplication, JobPost
from .forms import JobPostForm
from django.contrib.auth import logout
from django.contrib import messages


# List all active job posts
def job_list(request):
    jobs = JobPost.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

# View a single job post
def job_detail(request, pk):
    job = get_object_or_404(JobPost, pk=pk)  # Assuming `JobPost` is your model
    is_job_seeker = False

    if request.user.is_authenticated:
        # Check if the user belongs to the 'JobSeeker' group
        is_job_seeker = JobSeeker.objects.filter(user=request.user).exists()




    context = {
        'job': job,
        'is_job_seeker': is_job_seeker,  # Pass this variable to the template
    }

    return render(request, 'jobs/job_detail.html', context)

# Create a new job post
@login_required
def job_create(request):
    # Check if the user has a JobSeeker or Employer profile
    try:
        # Check if the user is an employer
        employer = request.user.employer  # This will raise an exception if not an employer
    except Employer.DoesNotExist:
        return redirect('not_authorized')  # Redirect if the user is not an employer

    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user  # Associate the job with the logged-in employer
            job.save()
            return redirect('job_list')
    else:
        form = JobPostForm()

    return render(request, 'jobs/job_form.html', {'form': form})

# Update an existing job post
@login_required
def job_update(request, pk):
    job = get_object_or_404(JobPost, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_detail', pk=pk)
    else:
        form = JobPostForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form})

# Delete a job post
@login_required
def job_delete(request, pk):
    job = get_object_or_404(JobPost, pk=pk, created_by=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('job_list')
    return render(request, 'jobs/job_confirm_delete.html', {'job': job})


@login_required
def job_apply(request, pk):
    # Ensure the user is a Job Seeker
    if not JobSeeker.objects.filter(user=request.user).exists():
        messages.error(request, "Only Job Seekers can apply for jobs.")
        return redirect('job_detail', pk=pk)

    job = get_object_or_404(JobPost, pk=pk)

    # Check if the user already applied
    if JobApplication.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', pk=pk)

    # Save the application
    JobApplication.objects.create(user=request.user, job=job)
    messages.success(request, "You have successfully applied for the job.")
    return redirect('job_detail', pk=pk)



def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('job_list')  # Redirect to the job list or another page after logout
    return redirect('job_list')  # Handle the case if GET is used



def search_jobs(request):
    query = request.GET.get('q', '')  # Get the 'q' parameter from the GET request
    jobs = JobPost.objects.filter(title__icontains=query) if query else JobPost.objects.all()
    return render(request, 'jobs/search_results.html', {'jobs': jobs, 'query': query})
