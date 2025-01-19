from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from profilee.models import Employer, JobSeeker
from .models import JobApplication, JobPost
from .forms import JobApplicationForm, JobPostForm
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import FileResponse, HttpResponse
import os
import csv
import openpyxl




def export_all_applicants_excel(request):
    # Query to get all applicants (no filtering by job_id)
    applicants = JobApplication.objects.all()

    # Create a new Excel workbook and a sheet
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Applicants"

    # Add headers to the first row
    headers = ['Applicant Username', 'Job Title', 'Resume', 'Cover Letter', 'Applied At']
    sheet.append(headers)

    # Add the applicants data
    for applicant in applicants:
        row = [
            applicant.user.username,  # Applicant username
            applicant.job.title,  # Job title
            applicant.resume.name if applicant.resume else 'N/A',  # Resume file name or 'N/A'
            applicant.cover_letter if applicant.cover_letter else 'N/A',  # Cover letter or 'N/A'
            applicant.applied_at.strftime('%Y-%m-%d %H:%M:%S')  # Applied date formatted
        ]
        sheet.append(row)

    # Create the HTTP response with Excel content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="all_applicants.xlsx"'

    # Save the workbook to the response
    wb.save(response)

    return response


# List all active job posts
def job_list(request):
    jobs = JobPost.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

# View a single job post
def job_detail(request, pk):
    job = get_object_or_404(JobPost, pk=pk)  
    is_job_seeker = False
    is_employer = False

    if request.user.is_authenticated:
        # Check if the user belongs to the 'JobSeeker' group
        is_job_seeker = JobSeeker.objects.filter(user=request.user).exists()

    if request.user.is_authenticated:
        is_employer = Employer.objects.filter(user=request.user).exists()


    context = {
        'job': job,
        'is_job_seeker': is_job_seeker,  # Pass this variable to the template
        'is_employer': is_employer
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



def apply_job(request, job_id):
    job = JobPost.objects.get(id=job_id)
    
    # Check if the user has already applied for this job
    if JobApplication.objects.filter(user=request.user, job=job).exists():
        # If the user has already applied, show a message
        messages.info(request, 'You have already applied for this job.')
        return redirect('job_list')  # Redirect to the job list or appropriate page
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.user = request.user
            job_application.job = job
            job_application.full_name = form.cleaned_data['full_name']
            job_application.email = form.cleaned_data['email']
            job_application.phone_number = form.cleaned_data.get('phone_number', '')
            job_application.address = form.cleaned_data.get('address', '')
            job_application.save()

            messages.success(request, 'Your application has been successfully submitted!')
            return redirect('job_list')  # Adjust redirect as needed
        else:
            messages.error(request, 'There was an error with your application. Please try again.')
    else:
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
        }
        form = JobApplicationForm(initial=initial_data)
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})



def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('job_list')  # Redirect to the job list or another page after logout
    return redirect('job_list')  # Handle the case if GET is used



def search_jobs(request):
    query = request.GET.get('q', '')  # Get the 'q' parameter from the GET request
    jobs = JobPost.objects.filter(title__icontains=query) if query else JobPost.objects.all()
    return render(request, 'jobs/search_results.html', {'jobs': jobs, 'query': query})



def view_applicants(request, job_id):
    job = get_object_or_404(JobPost, pk=job_id)
    applicants = JobApplication.objects.filter(job=job)

    return render(request, 'jobs/view_applicants.html', {
        'job': job,
        'applicants': applicants,
    })






def all_applicants(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated

    # Fetch jobs created by the logged-in employer
    jobs = JobPost.objects.filter(created_by=request.user)

    # Get all applicants for those jobs
    applicants = JobApplication.objects.filter(job__in=jobs)

    # Add pagination
    paginator = Paginator(applicants, 7)  # Show 5 applicants per page
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Pass the paginated object to the template
    }
    return render(request, 'jobs/applicants_list.html', context)




# def download_resume(request, applicant_id):
#     applicant = Applicant.objects.get(id=applicant_id)
#     resume_path = applicant.resume.path
#     if os.path.exists(resume_path):
#         response = FileResponse(open(resume_path, 'rb'))
#         response['Content-Type'] = 'application/pdf'
#         response['Content-Disposition'] = f'attachment; filename={os.path.basename(resume_path)}'
#         return response
#     else:
#         return HttpResponse('Resume not found', status=404)

# def download_cover_letter(request, applicant_id):
#     applicant = Applicant.objects.get(id=applicant_id)
#     cover_letter_path = applicant.cover_letter.path
#     if os.path.exists(cover_letter_path):
#         response = FileResponse(open(cover_letter_path, 'rb'))
#         response['Content-Type'] = 'application/pdf'
#         response['Content-Disposition'] = f'attachment; filename={os.path.basename(cover_letter_path)}'
#         return response
#     else:
#         return HttpResponse('Cover letter not found', status=404)
    

def download_resume(request, application_id):
    try:
        application = JobApplication.objects.get(id=application_id)
        resume_path = application.resume.path
        
        if os.path.exists(resume_path):
            with open(resume_path, 'rb') as file:
                response = FileResponse(file)
                response['Content-Type'] = 'application/pdf'  # or set to another appropriate MIME type if needed
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(resume_path)}'
                return response
        else:
            return HttpResponse('Resume not found', status=404)
    except JobApplication.DoesNotExist:
        return HttpResponse('Application not found', status=404)
    

def download_cover_letter(request, application_id):
    try:
        application = JobApplication.objects.get(id=application_id)
        cover_letter = application.cover_letter
        
        if cover_letter:
            response = HttpResponse(cover_letter, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename="cover_letter_{application_id}.txt"'
            return response
        else:
            return HttpResponse('Cover letter not found', status=404)
    except JobApplication.DoesNotExist:
        return HttpResponse('Application not found', status=404)
    


def export_all_applicants_csv(request):
    # Query to get all applicants (no filtering by job_id)
    applicants = JobApplication.objects.all()
    
    # Create a response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_applicants.csv"'
    
    # Create a CSV writer object
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow(['Applicant Username', 'Job Title', 'Resume', 'Cover Letter', 'Applied At'])
    
    # Write the data rows
    for applicant in applicants:
        writer.writerow([
            applicant.user.username,  # Applicant username
            applicant.job.title,  # Job title
            applicant.resume.name if applicant.resume else 'N/A',  # Resume file name or 'N/A'
            applicant.cover_letter if applicant.cover_letter else 'N/A',  # Cover letter or 'N/A'
            applicant.applied_at.strftime('%Y-%m-%d %H:%M:%S')  # Applied date formatted
        ])
    
    return response


def export_all_applicants_excel(request):
    # Query to get all applicants (no filtering by job_id)
    applicants = JobApplication.objects.all()

    # Create a new Excel workbook and a sheet
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "Applicants"

    # Add headers to the first row
    headers = ['Applicant Username', 'Job Title', 'Resume', 'Cover Letter', 'Applied At']
    sheet.append(headers)

    # Add the applicants data
    for applicant in applicants:
        row = [
            applicant.user.username,  # Applicant username
            applicant.job.title,  # Job title
            applicant.resume.name if applicant.resume else 'N/A',  # Resume file name or 'N/A'
            applicant.cover_letter if applicant.cover_letter else 'N/A',  # Cover letter or 'N/A'
            applicant.applied_at.strftime('%Y-%m-%d %H:%M:%S')  # Applied date formatted
        ]
        sheet.append(row)

    # Create the HTTP response with Excel content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="all_applicants.xlsx"'

    # Save the workbook to the response
    wb.save(response)

    return response
