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
from studentdashboard.StudentLoginRequiredMixin import StudentLoginRequiredMixin
from codedictionapp.models import Subjects,Curriculum
from codedictiondashboard.forms import CurriculumForm

@method_decorator(group_required('Teacher', 'Student'), name='dispatch')
class CurriculumViews(StudentLoginRequiredMixin,DetailView):
    model = Subjects
    template_name = 'studentdashboard/courses/curriculum/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context    
@method_decorator(group_required('Teacher', 'Student'), name='dispatch')
class CurriculumDetailViews(StudentLoginRequiredMixin,DetailView):
    model = Curriculum
    template_name = 'studentdashboard/courses/curriculum/view.html'
    def get_object(self, queryset=None):
        return Curriculum.objects.get(slug=self.kwargs['curriculum_slug'])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context 