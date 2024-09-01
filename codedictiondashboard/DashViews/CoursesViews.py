import math
import readtime
import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from codedictiondashboard.decorators import group_required
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictionapp.models import SubjectType, Subjects, CourseCategories, Courses, CourseSubject
from codedictiondashboard.forms import CoursesForm, CourseSubjectOrderForm

@method_decorator(group_required('Teacher', 'Student'), name='dispatch')
class CoursesViews(CustomLoginRequiredMixin, ListView):
    paginate_by = 10
    model = Courses
    template_name = 'codedictiondashboard/courses/index.html'

    def get_queryset(self):
        queryset = Courses.objects.all()

        # Filtering by status (active/inactive)
        status = self.request.GET.get('status', None)
        if status is not None:
            if status == 'active':
                queryset = queryset.filter(status=True)
            elif status == 'inactive':
                queryset = queryset.filter(status=False)

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
        return context
    
@method_decorator(group_required('Teacher', 'Student'), name='dispatch')
class CoursesDetailViews(CustomLoginRequiredMixin, DetailView):
    model = Courses
    template_name = 'codedictiondashboard/courses/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
@method_decorator(group_required('Teacher', 'Student'), name='dispatch')
class CoursesCurriculumViews(CustomLoginRequiredMixin, DetailView):
    model = Courses
    template_name = 'codedictiondashboard/courses/curriculum.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        # Fetch subjects ordered by the 'order' field in CourseSubject model
        ordered_course_subjects = CourseSubject.objects.filter(course=course).order_by('order')

        context['course_subjects'] = ordered_course_subjects
        return context
    
@method_decorator(staff_member_required, name='dispatch')    
class AddCoursesViews(CustomLoginRequiredMixin, View):
    def get(self, request):
        course_categories = CourseCategories.objects.all()
        subjects = Subjects.objects.all()
        form = CoursesForm()
        return render(request, 'codedictiondashboard/courses/add.html', {
            'course_categories': course_categories,
            'subjects': subjects,
            'form': form
        })
    
    def post(self, request):
        form = CoursesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses')
        else:
            course_categories = CourseCategories.objects.all()
            subjects = Subjects.objects.all()
            return render(request, 'codedictiondashboard/courses/add.html', {
                'form': form,
                'course_categories': course_categories,
                'subjects': subjects
            })

@method_decorator(staff_member_required, name='dispatch')
class EditCoursesViews(CustomLoginRequiredMixin, View):
    def get(self, request, course_id):
        course = get_object_or_404(Courses, pk=course_id)
        form = CoursesForm(instance=course)
        course_categories = CourseCategories.objects.all()
        subjects = Subjects.objects.all()
        return render(request, 'codedictiondashboard/courses/edit.html', {
            'form': form,
            'course_categories': course_categories,
            'subjects': subjects,
            'course': course
        })
    
    def post(self, request, course_id):
        course = get_object_or_404(Courses, pk=course_id)
        form = CoursesForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses')
        else:
            course_categories = CourseCategories.objects.all()
            subjects = Subjects.objects.all()
            return render(request, 'codedictiondashboard/courses/edit.html', {
                'form': form,
                'course_categories': course_categories,
                'subjects': subjects,
                'course': course
            })
        
@method_decorator(staff_member_required, name='dispatch')
class DeleteCoursesViews(CustomLoginRequiredMixin, View):
    def get(self, request, category_id):
        course = get_object_or_404(Courses, pk=category_id)
        course.delete()
        result = {
            'status': True
        }
        return JsonResponse(result, safe=False)

@method_decorator(staff_member_required, name='dispatch')
class UpdateCourseSubjectsOrder(CustomLoginRequiredMixin, FormView):
    template_name = 'codedictiondashboard/courses/update-course-subjects-order.html'
    form_class = CourseSubjectOrderForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        course = get_object_or_404(Courses, id=self.kwargs['course_id'])
        kwargs['course'] = course
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Courses, id=self.kwargs['course_id'])
        context['course'] = course
        return context
    
    def form_valid(self, form):
        course = get_object_or_404(Courses, id=self.kwargs['course_id'])
        existing_subject_ids = set()
        
        for key, value in form.cleaned_data.items():
            if key.startswith('order_new_'):
                try:
                    subject_id = int(key.split('_')[2])
                    if subject_id not in existing_subject_ids:
                        course_subject = CourseSubject(
                            course=course,
                            subject_id=subject_id,
                            order=value
                        )
                        course_subject.save()
                except ValueError:
                    continue  # Ignore if the conversion fails
            elif key.startswith('order_'):
                try:
                    subject_id = int(key.split('_')[1])
                    course_subject = CourseSubject.objects.get(id=subject_id, course=course)
                    course_subject.order = value
                    course_subject.save()
                    existing_subject_ids.add(subject_id)
                except CourseSubject.DoesNotExist:
                    continue
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('app.dashboard.courses.view', kwargs={'course_id': self.kwargs['course_id']})

@method_decorator(staff_member_required, name='dispatch')
class StatusCoursesViews(CustomLoginRequiredMixin,View):
    def get(self, request, course_id):
        course = get_object_or_404(Courses, pk=course_id)
        if course.status == 1:
            course.status=0
        else:
            course.status=1
        course.save()        
        return redirect(request.META.get('HTTP_REFERER'))   