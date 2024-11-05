import math
import readtime
import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictionapp.models import SubjectType, Subjects, CourseCategories, Courses, CourseSubject
from codedictiondashboard.forms import CoursesForm
from django.contrib import messages
from django.db.models import Sum
from django.db.models import Q

@method_decorator(staff_member_required, name='dispatch')
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
        # Searching
        search = self.request.GET.get('q', None)
        if search is not None:
            search = search.strip()
            queryset = queryset.filter(
                Q(course_category__name__icontains=search) | 
                Q(subjects__name__icontains=search) | 
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
class CoursesDetailViews(CustomLoginRequiredMixin, DetailView):
    model = Courses
    template_name = 'codedictiondashboard/courses/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object 
        total_price = course.subjects.aggregate(total_price=Sum('price'))['total_price']
        total_price = total_price or 0
        # Calculate the discount percentage if applicable
        if total_price >= course.price:
            discount_percentage = round(((total_price - course.price) / total_price) * 100)
        else:
            discount_percentage = 0
        context['total_price'] = total_price
        context['discount_percentage'] = discount_percentage
        return context
    
@method_decorator(staff_member_required, name='dispatch')
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
            'form': form,
        })

    def post(self, request):
        form = CoursesForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save()  
            tags = request.POST.getlist('tags[]') 
            
            for tag in tags:
                try:
                    subject_id, order = map(int, tag.split('-'))
                    CourseSubject.objects.create(
                            course=course,
                            subject_id=subject_id,
                            order=order
                        )
                except (ValueError, CourseSubject.DoesNotExist):
                    continue

            messages.success(request, 'Course and subject order successfully added!')
            return redirect('app.dashboard.courses') 
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
        ordered_course_subjects = CourseSubject.objects.filter(course=course).order_by('order')
        return render(request, 'codedictiondashboard/courses/edit.html', {
            'form': form,
            'course_categories': course_categories,
            'subjects': subjects,
            'course': course,
            'ordered_course_subjects':ordered_course_subjects
        })
    
    def post(self, request, course_id):
        course = get_object_or_404(Courses, pk=course_id)
        form = CoursesForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save()  # Save the course first
            
            # Retrieve current CourseSubject records for this course
            current_course_subjects = CourseSubject.objects.filter(course=course)
            current_subject_ids = set(current_course_subjects.values_list('subject_id', flat=True))
            
            # Get subject and order from 'tags[]'
            new_subject_orders = request.POST.getlist('tags[]')
            new_subject_ids = set()

            for tag in new_subject_orders:
                try:
                    # Split the subject_id and order from the format 'subject_id-order'
                    subject_id, order = map(int, tag.split('-'))
                    new_subject_ids.add(subject_id)
                    
                    # If the subject already exists, update its order
                    if subject_id in current_subject_ids:
                        course_subject = CourseSubject.objects.get(course=course, subject_id=subject_id)
                        course_subject.order = order
                        course_subject.save()
                    else:
                        # Add new subject if it doesn't exist
                        CourseSubject.objects.create(course=course, subject_id=subject_id, order=order)
                except (ValueError, CourseSubject.DoesNotExist):
                    # Ignore invalid data or errors
                    continue

            # Remove subjects that are no longer in the updated list
            subjects_to_remove = current_subject_ids - new_subject_ids
            CourseSubject.objects.filter(course=course, subject_id__in=subjects_to_remove).delete()

            messages.success(request, 'Course and subject order successfully updated!')
            return redirect('app.dashboard.courses')
        else:
            # Re-render the page if form is invalid
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
class StatusCoursesViews(CustomLoginRequiredMixin,View):
    def get(self, request, course_id):
        course = get_object_or_404(Courses, pk=course_id)
        if course.status == 1:
            course.status=0
        else:
            course.status=1
        course.save()        
        return redirect(request.META.get('HTTP_REFERER'))