from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from codedictiondashboard.decorators import group_required

@login_required(login_url='/student/login/')
@group_required('Student')
def index(request):
        return render(request, 'studentdashboard/index.html')