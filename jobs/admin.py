from django.contrib import admin
from .models import JobPost

class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'job_type', 'application_deadline', 'is_active', 'created_at')
    list_filter = ('job_type', 'location', 'is_active', 'created_at')
    search_fields = ('title', 'company_name', 'location', 'description', 'requirements')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

admin.site.register(JobPost, JobPostAdmin)
