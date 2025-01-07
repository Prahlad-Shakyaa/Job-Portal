from django import forms
from .models import JobApplication, JobPost

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            'title',
            'company_name',
            'location',
            'job_type',
            'description',
            'requirements',
            'salary',
            'application_deadline'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter company name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job location'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter job description'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter job requirements'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter salary'}),
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume', 'cover_letter']