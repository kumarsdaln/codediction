import math
import readtime
import datetime
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictionapp.models import Courses, OurBatch
from codedictiondashboard.forms import OurBatchForm

@method_decorator(staff_member_required, name='dispatch')
class OurBatchViews(CustomLoginRequiredMixin,ListView):
    model = OurBatch
    template_name = 'codedictiondashboard/courses/batches/index.html'
    queryset = OurBatch.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
@method_decorator(staff_member_required, name='dispatch')    
class OurBatchDetailViews(CustomLoginRequiredMixin,DetailView):
    model = OurBatch
    template_name = 'codedictiondashboard/courses/batches/view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context     
        
@method_decorator([csrf_exempt, staff_member_required], name='dispatch') 
class AddOurBatchViews(CustomLoginRequiredMixin,View):

    def get(self, request):
        courses = Courses.objects.all()
        return render(request, 'codedictiondashboard/courses/batches/add.html',{
            'courses':courses
        })
    
    @method_decorator(csrf_protect)
    def post(self, request):
        form = OurBatchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses')
        else:
            courses = Courses.objects.all()
            return render(request, 'codedictiondashboard/courses/batches/add.html', {
                'form':form,
                'courses':courses
            })  
    
@method_decorator([csrf_exempt, staff_member_required], name='dispatch') 
class EditOurBatchViews(CustomLoginRequiredMixin,View):  
    def get(self, request, batch_id):
        ourbatch= get_object_or_404(OurBatch, pk=batch_id)
        form = OurBatchForm(instance=ourbatch)
        courses = Courses.objects.all()
        return render(request, 'codedictiondashboard/courses/batches/edit.html',{
            'form':form,
            'courses':courses,
            'ourbatch':ourbatch
        })
    
    @method_decorator(csrf_protect)
    def post(self, request, batch_id):
        ourbatch= get_object_or_404(OurBatch, pk=batch_id)
        form = OurBatchForm(request.POST, request.FILES, instance=ourbatch)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.courses')
        else:
            courses = Courses.objects.all()
            return render(request, 'codedictiondashboard/courses/batches/edit.html', {
                'form':form,
                'courses':courses,
                'ourbatch':ourbatch
            })    

@method_decorator(staff_member_required, name='dispatch')    
class DeleteOurBatchViews(CustomLoginRequiredMixin,View):
    def get(self, request, batch_id):
        ourbatch = get_object_or_404(OurBatch, pk=batch_id)
        ourbatch.delete()
        result = {
            'status':True
        }
        return JsonResponse(result, safe=False)  