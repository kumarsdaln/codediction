from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from codedictiondashboard.decorators import group_required
from studentdashboard.StudentLoginRequiredMixin import StudentLoginRequiredMixin
from codedictionapp.models import Courses, CourseSubject, CourseCategories
from studentdashboard.models import Enrollment
from studentdashboard.forms import EnrollmentForm
from django.db.models import Q
from django.views import View
from django.db.models import Sum

@method_decorator(group_required('Student'), name='dispatch')
class CoursesViews(StudentLoginRequiredMixin, ListView):
    paginate_by = 10
    model = Courses
    template_name = 'studentdashboard/courses/index.html'

    def get_queryset(self):
        queryset = Courses.objects.filter(status=True)

        # Filtering by category
        category_slugs = self.request.GET.getlist('category', ['all'])
        if 'all' not in category_slugs:
            queryset = queryset.filter(
                Q(course_category__slug__in=category_slugs)
            )
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
        context["categories"] = CourseCategories.objects.all()
        context['selected_categories'] = self.request.GET.getlist('category', ['all'])
        context['q'] = self.request.GET.get('q', None)
        return context
    
@method_decorator(group_required('Student'), name='dispatch')
class CoursesDetailViews(StudentLoginRequiredMixin, DetailView):
    model = Courses
    template_name = 'studentdashboard/courses/view.html'

    def get_context_data(self, **kwargs):
        student_profile = self.request.user.student_profile
        context = super().get_context_data(**kwargs)
        course = self.object 
        total_price = course.subjects.aggregate(total_price=Sum('price'))['total_price']
        enrolled = Enrollment.objects.filter(student=student_profile, course=course).exists()
        total_price = total_price or 0
        # Calculate the discount percentage if applicable
        if total_price >= course.price:
            discount_percentage = round(((total_price - course.price) / total_price) * 100)
        else:
            discount_percentage = 0
        context['total_price'] = total_price
        context['discount_percentage'] = discount_percentage
        context['enrolled'] = enrolled
        return context
    
@method_decorator(group_required('Student'), name='dispatch')
class CoursesCurriculumViews(StudentLoginRequiredMixin, DetailView):
    model = Courses
    template_name = 'studentdashboard/courses/curriculum.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        # Fetch subjects ordered by the 'order' field in CourseSubject model
        ordered_course_subjects = CourseSubject.objects.filter(course=course).order_by('order')

        context['course_subjects'] = ordered_course_subjects
        return context   