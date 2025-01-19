from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from profilee.models import Employer
from .models import Blog
from .forms import BlogForm

def blog_list(request):
    posts = Blog.objects.all().order_by('-published_date')
    employer = request.user.groups.filter(name="Employer").exists() if request.user.is_authenticated else False
    return render(request, 'blog/blog_list.html', {'posts': posts, 'employer': employer})


def blog_detail(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'post': post})

@login_required
def blog_create(request):
    try:
        # Check if the user is an employer
        employer = request.user.employer  # This will raise an exception if not an employer
    except Employer.DoesNotExist:
        return redirect('not_authorized')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'blog/blog_form.html', {'form': form})


@login_required
def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog_list')
    return render(request, 'blog/blog_confirm_delete.html', {'blog': blog})
