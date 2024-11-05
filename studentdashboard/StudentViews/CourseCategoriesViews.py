from django.utils.decorators import method_decorator
from codedictiondashboard.decorators import group_required
from django.views.generic import ListView
from studentdashboard.StudentLoginRequiredMixin import StudentLoginRequiredMixin
from codedictionapp.models import CourseCategories

@method_decorator(group_required('Student'), name='dispatch')
class CourseCategoriesViews(StudentLoginRequiredMixin,ListView):
    model = CourseCategories
    template_name = 'studentdashboard/courses/category/index.html'
    queryset = CourseCategories.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context