from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from codedictiondashboard.decorators import group_required
from studentdashboard.StudentLoginRequiredMixin import StudentLoginRequiredMixin
from codedictionapp.models import Courses, CourseCategories
from studentdashboard.models import Enrollment
from studentdashboard.forms import EnrollmentForm
from django.db.models import Q
from django.views import View

@method_decorator(group_required('Student'), name='dispatch')
class CourseEnrollmentView(StudentLoginRequiredMixin, View):
    def post(self, request, slug):
        course = get_object_or_404(Courses, slug=slug)
        student_profile = request.user.student_profile

        # Check if the student is already enrolled in the course
        if Enrollment.objects.filter(student=student_profile, course=course).exists():
            return render(request, 'studentdashboard/courses/view.html', {
                'courses': course,
                'form': EnrollmentForm(),
                'error': 'You are already enrolled in this course.'
            })

        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save(student=student_profile)
            return redirect('app.student.courses')

        return render(request, 'studentdashboard/courses/view.html', {
            'courses': course,
            'form': form
        })

@method_decorator(group_required('Student'), name='dispatch')
class EnrolledCoursesView(StudentLoginRequiredMixin, ListView):
    paginate_by = 10
    model = Enrollment
    template_name = 'studentdashboard/courses/enrolled.html'

    def get_queryset(self):
        student_profile = self.request.user.student_profile
        queryset = Enrollment.objects.filter(student=student_profile)

        category_slugs = self.request.GET.getlist('category', ['all'])
        if 'all' not in category_slugs:
            queryset = queryset.filter(
                Q(course__course_category__slug__in=category_slugs)
            )
        # Searching
        search = self.request.GET.get('q', None)
        if search is not None:
            search = search.strip()
            queryset = queryset.filter(
                Q(course__course_category__name__icontains=search) | 
                Q(course__subjects__name__icontains=search) | 
                Q(course__name__icontains=search) |
                Q(course__description__icontains=search)
            ).distinct()
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