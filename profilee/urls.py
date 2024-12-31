from django.urls import path
from . import views

urlpatterns = [
    path('role-selection/', views.role_selection, name='role_selection'),

    path('job-seeker-profile/', views.job_seeker_profile, name='job_seeker_profile'), 
    path('edit-job-seeker-profile/', views.edit_job_seeker_profile, name='edit_job_seeker_profile'),

    path('employer-profile/', views.employer_profile, name='employer_profile'),  # Employer Profile
    path('edit-employer-profile/', views.edit_employer_profile, name='edit_employer_profile'),


]
