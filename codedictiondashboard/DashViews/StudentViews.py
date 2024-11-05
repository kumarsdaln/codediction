from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from studentdashboard.models import StudentProfile, Education
from django.contrib.auth.models import User
from codedictiondashboard.forms import StudentProfileForm, EducationForm
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.db.models import Q

@method_decorator(staff_member_required, name='dispatch')
class StudentViews(CustomLoginRequiredMixin, ListView):
    paginate_by = 10
    model = StudentProfile
    template_name = 'codedictiondashboard/students/index.html'

    def get_queryset(self):
        queryset = StudentProfile.objects.all()

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
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(designation__icontains=search) |
                Q(phone__icontains=search)
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
class StudentDetailViews(CustomLoginRequiredMixin, DetailView):
    model = StudentProfile
    template_name = 'codedictiondashboard/students/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
# @method_decorator(staff_member_required, name='dispatch')    
# class AddCoursesViews(CustomLoginRequiredMixin, View):
#     def get(self, request):
#         form = CoursesForm()
#         return render(request, 'codedictiondashboard/courses/add.html', {
#             'form': form
#         })
    
#     def post(self, request):
#         form = CoursesForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('app.dashboard.courses')
#         else:
#             return render(request, 'codedictiondashboard/courses/add.html', {
#                 'form': form,
#             })

@method_decorator(staff_member_required, name='dispatch')
class EditStudentViews(CustomLoginRequiredMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'codedictiondashboard/students/edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.get_object().user})
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_object(self):
        return StudentProfile.objects.get(id=self.kwargs['student_id']) 
    
    def get_success_url(self):
        messages.success(self.request, 'Student profile successfully updated!')
        return self.request.META.get('HTTP_REFERER', reverse_lazy('app.dashboard'))
        
# @method_decorator(staff_member_required, name='dispatch')
# class DeleteCoursesViews(CustomLoginRequiredMixin, View):
#     def get(self, request, category_id):
#         course = get_object_or_404(StudentProfile, pk=category_id)
#         course.delete()
#         result = {
#             'status': True
#         }
#         return JsonResponse(result, safe=False)

@method_decorator(staff_member_required, name='dispatch')
class StatusStudentViews(CustomLoginRequiredMixin,View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        if user.is_active == 1:
            user.is_active=0
        else:
            user.is_active=1
        user.save()        
        return redirect(request.META.get('HTTP_REFERER'))   
    
@method_decorator(staff_member_required, name='dispatch')    
class StudentPasswordChangeView(CustomLoginRequiredMixin, View):
    template_name = 'codedictiondashboard/students/password-change.html'

    def get(self, request, *args, **kwargs):
        # Get the student profile and the associated user
        student_profile = get_object_or_404(StudentProfile, pk=self.kwargs['student_id'])
        form = SetPasswordForm(user=student_profile.user)  # Render an empty password form
        return render(request, self.template_name, {'form': form, 'object': student_profile})

    def post(self, request, *args, **kwargs):
        # Get the student profile and the associated user
        student_profile = get_object_or_404(StudentProfile, pk=self.kwargs['student_id'])
        form = SetPasswordForm(user=student_profile.user, data=request.POST)

        if form.is_valid():
            form.save()  # Save the new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect(request.META.get('HTTP_REFERER', 'app.dashboard'))  # Redirect back or to the dashboard
        else:
            # If the form is invalid, render the form with errors
            return render(request, self.template_name, {'form': form, 'object': student_profile})

    
class StudentEducationManageView(View):
    def get(self, request, pk=None, *args, **kwargs):
        education_records = Education.objects.order_by('-id').all()
        object = StudentProfile.objects.get(id=self.kwargs['student_id'])
        # Adding a new record
        form = EducationForm(student_profile=object)
        return render(request, 'codedictiondashboard/students/education.html', {
            'form': form,
            'object':object,
            'education_records':education_records
        })

    def post(self, request, pk=None, *args, **kwargs):
        student_profile = StudentProfile.objects.get(id=self.kwargs['student_id'])
        if 'delete' in request.POST and pk:
            # Delete action
            education_record = get_object_or_404(Education, pk=pk)
            education_record.delete()
            messages.success(request, 'Education successfully deleted!')
            return redirect(self.request.META.get('HTTP_REFERER', reverse_lazy('app.dashboard')))  # Redirect to the list view
        
        if pk:
            # Edit action
            education_record = get_object_or_404(Education, pk=pk)
            form = EducationForm(request.POST, instance=education_record, student_profile=student_profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Education successfully updated!')
                return redirect(self.request.META.get('HTTP_REFERER', reverse_lazy('app.dashboard')))  # Redirect to the list view
            return render(request, 'studentdashboard/profile/education.html', {'form': form, 'education_record': education_record})
        
        # Add action
        form = EducationForm(request.POST, student_profile=student_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'New educatoin added!')
            return redirect(self.request.META.get('HTTP_REFERER', reverse_lazy('app.dashboard')))  # Redirect to the list view
        return render(request, 'studentdashboard/profile/education.html', {'form': form})    