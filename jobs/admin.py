from django.contrib import admin
from .models import JobApplication, JobPost

class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'job_type', 'application_deadline', 'is_active', 'created_at')
    list_filter = ('job_type', 'location', 'is_active', 'created_at')
    search_fields = ('title', 'company_name', 'location', 'description', 'requirements')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

admin.site.register(JobPost, JobPostAdmin)


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'applied_at')  # Columns to display in the admin list view
    list_filter = ('applied_at', 'job')  # Filters for the right-hand sidebar
    search_fields = ('user__username', 'job__title')  # Search by related user and job title
    ordering = ('-applied_at',)  # Order by most recent application by default

admin.site.register(JobApplication, JobApplicationAdmin)