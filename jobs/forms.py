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


# class JobApplicationForm(forms.ModelForm):
#     class Meta:
#         model = JobApplication
#         fields = ['resume', 'cover_letter']


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'full_name',
            'email',
            'phone_number',
            'address',
            'resume',
            'cover_letter'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number' }),
            'address': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Enter your address', 'rows': 3 }),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Write your cover letter here...', 'rows': 4}),
        }
