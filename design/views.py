from django.shortcuts import render

from jobs.models import JobPost

def homepage(request):
    jobs = JobPost.objects.order_by('-created_at')[:3]
    return render(request, 'design/homepage/index.html',{'jobs':jobs})
