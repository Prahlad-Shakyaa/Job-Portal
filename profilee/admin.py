from django.contrib import admin
from .models import JobSeeker, Employer

class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'phone_number', 'location', 'education', 'role', 'resume', 'cover_letter', 'image')
    list_filter = ('role', 'location')
    search_fields = ('user__username', 'name', 'email', 'phone_number')
    ordering = ('user',)
    readonly_fields = ('user',)  # Make the user field read-only as it's a foreign key

    # You can customize the form if needed
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'email', 'phone_number', 'location', 'education', 'role', 'resume', 'cover_letter', 'image')
        }),
    )


admin.site.register(JobSeeker, JobSeekerAdmin)

class EmployerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_description', 'website_url', 'location', 'contact_number')
    list_filter = ('location',)  # Add more filters as needed, such as company name or location
    search_fields = ('user__username', 'company_name', 'website_url', 'location', 'contact_number')
    ordering = ('user',)  # Default ordering by user
    readonly_fields = ('user',)  # Make the user field read-only as it's a foreign key

    # You can customize the form if needed
    fieldsets = (
        (None, {
            'fields': ('user', 'company_name', 'company_description', 'website_url', 'location', 'contact_number')
        }),
    )

admin.site.register(Employer, EmployerAdmin)
