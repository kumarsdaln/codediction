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
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictionapp.models import SubjectType, Subjects, CourseCategories, Courses, CourseSubject
from codedictiondashboard.forms import CoursesForm, CourseSubjectOrderForm

class CoursesViews(CustomLoginRequiredMixin, ListView):
    model = Courses
    template_name = 'codedictiondashboard/courses/index.html'
    queryset = Courses.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CoursesDetailViews(CustomLoginRequiredMixin, DetailView):
    model = Courses
    template_name = 'codedictiondashboard/courses/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

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

class DeleteCoursesViews(CustomLoginRequiredMixin, View):
    def get(self, request, category_id):
        course = get_object_or_404(Courses, pk=category_id)
        course.delete()
        result = {
            'status': True
        }
        return JsonResponse(result, safe=False)

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
        return reverse('course_detail', kwargs={'course_id': self.kwargs['course_id']})



