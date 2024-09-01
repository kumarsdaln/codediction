from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from codedictiondashboard.forms import RegistrationForm

class RegisterView(FormView):
    template_name = 'codedictiondashboard/register/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
