import math
from typing import Any
from django.db.models.query import QuerySet
import json
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
from codedictionapp.models import SubjectType,Subjects, Curriculum
from codedictiondashboard.forms import SubjectsForm
from django.db.models import Q
@method_decorator(staff_member_required, name='dispatch')
class SubjectsViews(CustomLoginRequiredMixin,ListView):
    paginate_by = 12
    model = Subjects
    template_name = 'codedictiondashboard/courses/subjects/index.html'

    def get_queryset(self):
        queryset = Subjects.objects.all()

         # Searching
        search = self.request.GET.get('q', None)
        if search is not None:
            search = search.strip()
            queryset = queryset.filter(
                Q(subject_type__name__icontains=search) |
                Q(name__icontains=search) |
                Q(description__icontains=search)
            ).distinct()
        # Sorting by 'id' or 'title' with direction
        sort_by = self.request.GET.get('sort_by', 'id')
        sort_direction = self.request.GET.get('sort_direction', 'desc')

        if sort_by in ['id', 'name']:
            if sort_direction == 'asc':
                queryset = queryset.order_by(sort_by)
            else:
                queryset = queryset.order_by(f'-{sort_by}')
        return queryset
    def get(self, request, *args, **kwargs):
        current_page = request.GET.get('page', 1)
        total_pages = self.get_paginator(self.get_queryset(), self.paginate_by).num_pages
        if int(current_page) > int(total_pages):
            return redirect(f'{self.request.path}?page={total_pages}')
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_results"] = self.get_queryset().count()
        context['q'] = self.request.GET.get('q', None)
        return context
    
@method_decorator(staff_member_required, name='dispatch')
class SubjectsDetailViews(CustomLoginRequiredMixin,DetailView):
    model = Subjects
    template_name = 'codedictiondashboard/courses/subjects/view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context     
@method_decorator(staff_member_required, name='dispatch')
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
    
class UpdateCurriculumOrderViews(CustomLoginRequiredMixin, View):
    def post(self, request, slug):
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            for item in data:
                curriculum_id = item.get('id')
                new_order = item.get('order')

                # Update the curriculum order in the database
                Curriculum.objects.filter(id=curriculum_id).update(order=new_order)

            return JsonResponse({'success': True})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)