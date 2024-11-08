# Generated by Django 5.1 on 2024-09-09 09:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codedictionapp', '0025_socialmediaplatform'),
        ('studentdashboard', '0002_education'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField(max_length=1000)),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_social_platforms', to='codedictionapp.socialmediaplatform')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_social_media', to='studentdashboard.studentprofile')),
            ],
        ),
    ]
