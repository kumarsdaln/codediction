import math
import readtime
import datetime
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.core.paginator import Paginator
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictionapp.models import SubjectType
from codedictiondashboard.forms import SubjectTypeForm

class SubjectTypeViews(CustomLoginRequiredMixin,ListView):
    model = SubjectType
    template_name = 'codedictiondashboard/courses/subjects/type/index.html'
    queryset = SubjectType.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
@method_decorator(csrf_exempt, name="dispatch") 
class AddSubjectTypeViews(CustomLoginRequiredMixin,View):

    # def get(self, request):
    #     return render(request, 'codedictiondashboard/blog/add.html')    
    
    @method_decorator(csrf_protect)
    def post(self, request):
        form = SubjectTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses.subjects.type')
        else:
            return render(request, 'codedictiondashboard/courses/subjects/type/index.html', {
                'form':form
            })  
    
@method_decorator(csrf_exempt, name="dispatch") 
class EditSubjectTypeViews(CustomLoginRequiredMixin,View):  
    
    @method_decorator(csrf_protect)
    def post(self, request, subject_type_id):
        subjectType = get_object_or_404(SubjectType, pk=subject_type_id)
        form = SubjectTypeForm(request.POST,instance=subjectType)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses.subjects.type')
        else:
            return render(request, 'codedictiondashboard/courses/subjects/type/index.html', {
                'form':form
            })    
    
class DeleteSubjectTypeViews(CustomLoginRequiredMixin,View):
    def get(self, request, category_id):
        category = get_object_or_404(SubjectType, pk=category_id)
        category.delete()
        result = {
            'status':True
        }
        return JsonResponse(result, safe=False)  