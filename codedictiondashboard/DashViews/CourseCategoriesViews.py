from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from codedictiondashboard.decorators import group_required
from django.views import View
from django.views.generic import ListView
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictionapp.models import CourseCategories
from codedictiondashboard.forms import CourseCategoriesForm

@method_decorator(staff_member_required, name='dispatch')
class CourseCategoriesViews(CustomLoginRequiredMixin,ListView):
    model = CourseCategories
    template_name = 'codedictiondashboard/courses/category/index.html'
    queryset = CourseCategories.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
@method_decorator([csrf_exempt, staff_member_required], name="dispatch") 
class AddCourseCategoriesViews(CustomLoginRequiredMixin,View):

    # def get(self, request):
    #     return render(request, 'codedictiondashboard/blog/add.html')    
    
    @method_decorator(csrf_protect)
    def post(self, request):
        form = CourseCategoriesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return render(request, 'app.dashboard.courses.category', {
                'form':form
            })  
    
@method_decorator([csrf_exempt, staff_member_required], name="dispatch") 
class EditCourseCategoriesViews(CustomLoginRequiredMixin,View):  
    
    @method_decorator(csrf_protect)
    def post(self, request, category_id):
        category = get_object_or_404(CourseCategories, pk=category_id)
        form = CourseCategoriesForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses.category')
        else:
            return render(request, 'app.dashboard.courses.category', {
                'form':form
            })   
@method_decorator(staff_member_required, name='dispatch')    
class DeleteCourseCategoriesViews(CustomLoginRequiredMixin,View):
    def get(self, request, category_id):
        category = get_object_or_404(CourseCategories, pk=category_id)
        category.delete()
        result = {
            'status':True
        }
        return JsonResponse(result, safe=False)  