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
from codedictionapp.models import Subjects,Curriculum
from codedictiondashboard.forms import CurriculumForm

class CurriculumViews(CustomLoginRequiredMixin,DetailView):
    model = Subjects
    template_name = 'codedictiondashboard/courses/curriculum/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context    
class CurriculumDetailViews(CustomLoginRequiredMixin,DetailView):
    model = Curriculum
    template_name = 'codedictiondashboard/courses/curriculum/view.html'
    def get_object(self, queryset=None):
        return Curriculum.objects.get(slug=self.kwargs['curriculum_slug'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context  
        
@method_decorator(csrf_exempt, name="dispatch") 
class AddCurriculumViews(CustomLoginRequiredMixin,View):

    def get(self, request, slug):
        subject = get_object_or_404(Subjects, slug=slug)
        form = CurriculumForm()
        return render(request, 'codedictiondashboard/courses/curriculum/add.html',{
            'subject':subject
        })
    
    @method_decorator(csrf_protect)
    def post(self, request, slug):
        subject = get_object_or_404(Subjects, slug=slug)
        form = CurriculumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses.subjects.curriculum.details',slug=subject.slug, curriculum_slug=request.POST.get('slug'))
        else:
            return render(request, 'codedictiondashboard/courses/curriculum/add.html', {
                'form':form,
                'subject':subject
            })  
@method_decorator(csrf_exempt, name="dispatch") 
class AddRelCurriculumViews(CustomLoginRequiredMixin,View):

    def get(self, request, slug, rel_cur_slug):
        subject = get_object_or_404(Subjects, slug=slug)
        related_currculum = get_object_or_404(Curriculum, slug=rel_cur_slug)
        form = CurriculumForm()
        return render(request, 'codedictiondashboard/courses/curriculum/add.html',{
            'subject':subject,
            'related_currculum':related_currculum
        })
    
    @method_decorator(csrf_protect)
    def post(self, request, slug,rel_cur_slug):
        subject = get_object_or_404(Subjects, slug=slug)
        related_currculum = get_object_or_404(Curriculum, slug=rel_cur_slug)
        form = CurriculumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses.subjects.curriculum.details',slug=subject.slug, curriculum_slug=request.POST.get('slug'))
        else:
            return render(request, 'codedictiondashboard/courses/curriculum/add.html', {
                'form':form,
                'subject':subject
            })    
@method_decorator(csrf_exempt, name="dispatch") 
class EditCurriculumViews(CustomLoginRequiredMixin,View):  
    def get(self, request, slug, curriculum_slug):
        curriculum= get_object_or_404(Curriculum, slug=curriculum_slug)
        form = CurriculumForm(instance=curriculum)
        subjects = Subjects.objects.all()
        return render(request, 'codedictiondashboard/courses/curriculum/edit.html',{
            'form':form,
            'subjects':subjects,
            'curriculum':curriculum
        })
    
    @method_decorator(csrf_protect)
    def post(self, request, slug, curriculum_slug):
        curriculum= get_object_or_404(Curriculum, slug=curriculum_slug)
        form = CurriculumForm(request.POST, request.FILES, instance=curriculum)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses.subjects.curriculum.details',slug=slug, curriculum_slug=request.POST.get('slug'))
        else:
            subjects = Subjects.objects.all()
            return render(request, 'codedictiondashboard/courses/curriculum/edit.html', {
                'form':form,
                'subjects':subjects,
                'curriculum':curriculum
            })    
    
class DeleteCurriculumViews(CustomLoginRequiredMixin,View):
    def get(self, request, curriculum_id):
        curriculum = get_object_or_404(Curriculum, pk=curriculum_id)
        curriculum.delete()
        result = {
            'status':True
        }
        return JsonResponse(result, safe=False)  