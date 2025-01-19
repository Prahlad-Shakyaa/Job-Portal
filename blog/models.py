from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/')
    published_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/images/')
    published_date = models.DateField(auto_now_add=True)
    short_description = models.CharField(max_length=300)

    def __str__(self):
        return self.title
