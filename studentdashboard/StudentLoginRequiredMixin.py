from django.contrib.auth.mixins import LoginRequiredMixin

class StudentLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/student/login/'
