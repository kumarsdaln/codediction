from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from codedictionapp.models import Blog, Courses
from studentdashboard.models import StudentProfile, Enrollment

@login_required(login_url='/dashboard/login/')
def index(request):
        total_blog = Blog.objects.count()
        total_courses = Courses.objects.count()
        total_students = StudentProfile.objects.count()
        total_enrollments = Enrollment.objects.count()
        return render(request, 'codedictiondashboard/index.html', {
                'total_blog':total_blog,
                'total_courses':total_courses,
                'total_students':total_students,
                'total_enrollments':total_enrollments
        })