from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from studentdashboard.StudentLoginRequiredMixin import StudentLoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from studentdashboard.forms import StudentProfileForm, EducationForm
from studentdashboard.models import StudentProfile, Education
from codedictionapp.models import SocialMediaPlatform
from django.views import View
from django.contrib import messages

class ProfileView(StudentLoginRequiredMixin, DetailView):
    model = StudentProfile
    template_name = 'studentdashboard/profile/index.html'

    def get_object(self):
        return self.request.user.student_profile
    
class ProfileEditView(StudentLoginRequiredMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'studentdashboard/profile/edit.html'
    success_url = reverse_lazy('/student/')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['social_media_platforms'] = SocialMediaPlatform.objects.all()
        return context
    def get_object(self, queryset=None):
        return self.request.user.student_profile
    
class StudentPasswordChangeView(StudentLoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('app.student.profile.password-change')
    template_name = 'studentdashboard/profile/password-change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.request.user.student_profile
        return context
    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)
    
class EducationManageView(StudentLoginRequiredMixin, View):
    def get(self, request, pk=None, *args, **kwargs):
        education_records = Education.objects.order_by('-id').all()
        object = self.request.user.student_profile
        # Adding a new record
        form = EducationForm(student_profile=request.user.student_profile)
        return render(request, 'studentdashboard/profile/education.html', {
            'form': form,
            'object':object,
            'education_records':education_records
        })

    def post(self, request, pk=None, *args, **kwargs):
        if 'delete' in request.POST and pk:
            # Delete action
            education_record = get_object_or_404(Education, pk=pk)
            education_record.delete()
            return redirect('app.student.profile.education')  # Redirect to the list view
        
        if pk:
            # Edit action
            education_record = get_object_or_404(Education, pk=pk)
            form = EducationForm(request.POST, instance=education_record, student_profile=request.user.student_profile)
            if form.is_valid():
                form.save()
                return redirect('app.student.profile.education')  # Redirect to the list view
            return render(request, 'studentdashboard/profile/education.html', {'form': form, 'education_record': education_record})
        
        # Add action
        form = EducationForm(request.POST, student_profile=request.user.student_profile)
        if form.is_valid():
            form.save()
            return redirect('app.student.profile.education')  # Redirect to the list view
        return render(request, 'studentdashboard/profile/education.html', {'form': form})    