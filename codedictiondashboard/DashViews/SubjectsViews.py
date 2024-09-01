import math
import readtime
import datetime
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from codedictiondashboard.decorators import group_required
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictionapp.models import SubjectType,Subjects
from codedictiondashboard.forms import SubjectsForm
@method_decorator(group_required('Teacher', 'Student'), name='dispatch')
class SubjectsViews(CustomLoginRequiredMixin,ListView):
    model = Subjects
    template_name = 'codedictiondashboard/courses/subjects/index.html'
    queryset = Subjects.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
@method_decorator(group_required('Teacher', 'Student'), name='dispatch')
class SubjectsDetailViews(CustomLoginRequiredMixin,DetailView):
    model = Subjects
    template_name = 'codedictiondashboard/courses/subjects/view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context     
@method_decorator(group_required('Teacher', 'Student'), name='dispatch')
class SubjectsCurriculumViews(CustomLoginRequiredMixin,DetailView):
    model = Subjects
    template_name = 'codedictiondashboard/courses/subjects/curriculum.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context     
@method_decorator([csrf_exempt, staff_member_required], name='dispatch') 
class AddSubjectsViews(CustomLoginRequiredMixin,View):

    def get(self, request):
        form = SubjectsForm()
        subject_types = SubjectType.objects.all()
        return render(request, 'codedictiondashboard/courses/subjects/add.html',{
            'subject_types':subject_types,
            'form':form
        })
    
    @method_decorator(csrf_protect)
    def post(self, request):
        form = SubjectsForm(request.POST, request.FILES)
        subject_types = SubjectType.objects.all()
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses.subjects')
        else:
            print(form.errors)
            return render(request, 'codedictiondashboard/courses/subjects/add.html', {
                'form':form,
                'subject_types':subject_types
            })  
    
@method_decorator([csrf_exempt, staff_member_required], name='dispatch') 
class EditSubjectsViews(CustomLoginRequiredMixin,View):  
    def get(self, request, subject_id):
        subject= get_object_or_404(Subjects, pk=subject_id)
        form = SubjectsForm(instance=subject)
        subject_types = SubjectType.objects.all()
        return render(request, 'codedictiondashboard/courses/subjects/edit.html',{
            'subject_types':subject_types,
            'form':form,
            'subject':subject
        })
    
    @method_decorator(csrf_protect)
    def post(self, request, subject_id):
        subject= get_object_or_404(Subjects, pk=subject_id)
        subject_types = SubjectType.objects.all()
        form = SubjectsForm(request.POST, request.FILES, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses.subjects')
        else:
            return render(request, 'codedictiondashboard/courses/subjects/edit.html', {
                'form':form,
                'subject_types':subject_types
            })    

@method_decorator(staff_member_required, name='dispatch')    
class DeleteSubjectTypeViews(CustomLoginRequiredMixin,View):
    def get(self, request, category_id):
        category = get_object_or_404(Subjects, pk=category_id)
        category.delete()
        result = {
            'status':True
        }
        return JsonResponse(result, safe=False)  