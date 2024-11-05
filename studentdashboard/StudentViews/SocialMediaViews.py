from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from studentdashboard.models import SocialMedia, StudentProfile
from studentdashboard.forms import SocialMediaForm
from studentdashboard.StudentLoginRequiredMixin import StudentLoginRequiredMixin

class SocialMediaView(StudentLoginRequiredMixin, View):
    def post(self, request, social_media_id=None):
        student_profile = request.user.student_profile
        
        if social_media_id:
            social_media = get_object_or_404(SocialMedia, id=social_media_id, student=student_profile)
            if 'delete' in request.POST:
                social_media.delete()
                return redirect('app.student.profile')
            form = SocialMediaForm(request.POST, instance=social_media)
        else:
            form = SocialMediaForm(request.POST)

        if form.is_valid():
            social_media = form.save(commit=False)
            social_media.student = student_profile
            social_media.save()
            return redirect('app.student.profile')
        return redirect('app.student.profile')
