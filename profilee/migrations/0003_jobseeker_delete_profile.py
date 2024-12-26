# Generated by Django 5.1.3 on 2024-12-25 03:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profilee', '0002_profile_image_alter_profile_education_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('education', models.TextField(blank=True)),
                ('email', models.EmailField(max_length=254)),
                ('role', models.CharField(max_length=100)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('cover_letter', models.FileField(blank=True, null=True, upload_to='cover_letters/')),
                ('image', models.ImageField(blank=True, null=True, upload_to='profile_pictures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]