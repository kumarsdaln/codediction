from django.utils.decorators import method_decorator
from codedictiondashboard.decorators import group_required
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from studentdashboard.StudentLoginRequiredMixin import StudentLoginRequiredMixin
from codedictionapp.models import Subjects
@method_decorator(group_required('Student'), name='dispatch')
class SubjectsViews(StudentLoginRequiredMixin,ListView):
    model = Subjects
    template_name = 'studentdashboard/courses/subjects/index.html'
    queryset = Subjects.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
@method_decorator(group_required('Student'), name='dispatch')
class SubjectsDetailViews(StudentLoginRequiredMixin,DetailView):
    model = Subjects
    template_name = 'studentdashboard/courses/subjects/view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context     
@method_decorator(group_required('Student'), name='dispatch')
class SubjectsCurriculumViews(StudentLoginRequiredMixin,DetailView):
    model = Subjects
    template_name = 'studentdashboard/courses/subjects/curriculum.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context     