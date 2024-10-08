# Generated by Django 5.1 on 2024-08-30 07:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codedictionapp', '0019_courses_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='codedictionapp.courses')),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=255, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(null=True, upload_to='uploads/student')),
                ('enrolled_courses', models.ManyToManyField(related_name='enrolled_students', through='codedictionapp.Enrollment', to='codedictionapp.courses')),
            ],
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=255, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(null=True, upload_to='uploads/student')),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('S', 'Student'), ('T', 'Teacher')], max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_type', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='EnrollStudent',
        ),
        migrations.DeleteModel(
            name='OurStudents',
        ),
        migrations.DeleteModel(
            name='OurTeam',
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='codedictionapp.studentprofile'),
        ),
        migrations.AddField(
            model_name='teacherprofile',
            name='user_type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_profile', to='codedictionapp.usertype'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='user_type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to='codedictionapp.usertype'),
        ),
    ]
