# Generated by Django 5.1.3 on 2025-01-01 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_jobapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='cover_letter',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='resume',
            field=models.FileField(default=1, upload_to='resumes/'),
            preserve_default=False,
        ),
    ]
