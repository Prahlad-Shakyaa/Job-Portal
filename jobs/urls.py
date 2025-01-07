from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/update/', views.job_update, name='job_update'),
    path('<int:pk>/delete/', views.job_delete, name='job_delete'),

    path('<int:job_id>/apply/', views.apply_job, name='job_apply'),

    path('<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),

    path('search/', views.search_jobs, name='search'),

    path('applicants/', views.all_applicants, name='all_applicants'),


    path('download_resume/<int:applicant_id>/', views.download_resume, name='download_resume'),
    path('download_cover_letter/<int:applicant_id>/', views.download_cover_letter, name='download_cover_letter'),  # New URL

    # path('export-csv/', views.export_applicants_csv, name='export_csv'),
    path('export_applicants/', views.export_all_applicants_csv, name='export_all_applicants_csv'),

    path('export_applicants_excel/', views.export_all_applicants_excel, name='export_all_applicants_excel')





]
