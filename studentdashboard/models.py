from django.db import models
from django.contrib.auth.models import User
import datetime
from codedictionapp.models import Courses, SocialMediaPlatform

# Create your models here.
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    designation = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=15, null=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='uploads/student', null=True)
    dob = models.DateField(null=True)
    location = models.TextField(null=True)
    joining_date = models.DateTimeField(default=datetime.datetime.now)
    enrolled_courses = models.ManyToManyField(Courses, through='Enrollment', related_name='enrolled_students')
    
    def __str__(self):
        return f"{self.user.username}"

class SocialMedia(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='student_social_media')
    platform = models.ForeignKey(SocialMediaPlatform, on_delete=models.CASCADE, related_name='student_social_platforms')
    link = models.TextField(max_length=1000)

class Education(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='student_education')
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"    
    
class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.user.username} - {self.course.name}'