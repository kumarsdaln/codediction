import math
import readtime
import datetime
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictionapp.models import SubjectType,Subjects,CourseCategories,Courses
from codedictiondashboard.forms import CoursesForm

class CoursesViews(CustomLoginRequiredMixin,ListView):
    model = Courses
    template_name = 'codedictiondashboard/courses/index.html'
    queryset = Courses.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
class CoursesDetailViews(CustomLoginRequiredMixin,DetailView):
    model = Courses
    template_name = 'codedictiondashboard/courses/view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context  
class CoursesCurriculumViews(CustomLoginRequiredMixin,DetailView):
    model = Courses
    template_name = 'codedictiondashboard/courses/curriculum.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context      
        
@method_decorator(csrf_exempt, name="dispatch") 
class AddCoursesViews(CustomLoginRequiredMixin,View):

    def get(self, request):
        course_categories = CourseCategories.objects.all()
        subjects = Subjects.objects.all()
        form = CoursesForm()
        return render(request, 'codedictiondashboard/courses/add.html',{
            'course_categories':course_categories,
            'subjects':subjects,
            'form':form
        })
    
    @method_decorator(csrf_protect)
    def post(self, request):
        form = CoursesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses')
        else:
            course_categories = CourseCategories.objects.all()
            subjects = Subjects.objects.all()
            return render(request, 'codedictiondashboard/courses/add.html', {
                'form':form,
                'course_categories':course_categories,
                'subjects':subjects
            })  
    
@method_decorator(csrf_exempt, name="dispatch") 
class EditCoursesViews(CustomLoginRequiredMixin,View):  
    def get(self, request, course_id):
        course= get_object_or_404(Courses, pk=course_id)
        form = CoursesForm(instance=course)
        course_categories = CourseCategories.objects.all()
        subjects = Subjects.objects.all()
        return render(request, 'codedictiondashboard/courses/edit.html',{
            'form':form,
            'course_categories':course_categories,
            'subjects':subjects,
            'course':course
        })
    
    @method_decorator(csrf_protect)
    def post(self, request, course_id):
        course= get_object_or_404(Courses, pk=course_id)
        form = CoursesForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses')
        else:
            course_categories = CourseCategories.objects.all()
            subjects = Subjects.objects.all()
            return render(request, 'codedictiondashboard/courses/edit.html', {
                'form':form,
                'course_categories':course_categories,
                'subjects':subjects
            })    
    
class DeleteCoursesViews(CustomLoginRequiredMixin,View):
    def get(self, request, category_id):
        course = get_object_or_404(Courses, pk=category_id)
        course.delete()
        result = {
            'status':True
        }
        return JsonResponse(result, safe=False)  