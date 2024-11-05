from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from django.urls import reverse_lazy

class ProfileView(CustomLoginRequiredMixin, DetailView):
    model = User
    template_name = 'codedictiondashboard/profile/index.html'
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user
    
class ProfileUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile_update.html'
    fields = ['first_name', 'last_name', 'email']  # Fields to be updated
    success_url = reverse_lazy('profile')  # Redirect to profile after update

    def get_object(self):
        # Returns the profile of the currently logged-in user
        return self.request.user