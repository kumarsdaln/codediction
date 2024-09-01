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
from django.core.paginator import Paginator
import math
import datetime
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictionapp.models import Services
from codedictiondashboard.forms import ServiceForm

@method_decorator(staff_member_required, name='dispatch')
class ServicesViews(CustomLoginRequiredMixin,ListView):
    model = Services
    template_name = 'codedictiondashboard/services/index.html'
    queryset = Services.objects.order_by('-id')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
@method_decorator(staff_member_required, name='dispatch')    
class ServicesDetailViews(CustomLoginRequiredMixin,DetailView):
    model = Services
    template_name = 'codedictiondashboard/services/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context    
    
@method_decorator([csrf_exempt, staff_member_required], name='dispatch') 
class AddServicesViews(CustomLoginRequiredMixin,View):

    def get(self, request):
        return render(request, 'codedictiondashboard/services/add.html')    
    
    @method_decorator(csrf_protect)
    def post(self, request):
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('app.dashboard.services')
        else:
            form = ServiceForm()
            return redirect(request.META.get('HTTP_REFERER'), {'form':form})  
    
@method_decorator([csrf_exempt, staff_member_required], name='dispatch') 
class EditServicesViews(CustomLoginRequiredMixin,View):

    def get(self, request, service_id):
        service = get_object_or_404(Services, pk=service_id)
        form = ServiceForm(instance=service)
        return render(request, 'codedictiondashboard/services/edit.html', {
            'form':form,
            'service':service,
        })    
    
    @method_decorator(csrf_protect)
    def post(self, request, service_id):
        service = get_object_or_404(Services, pk=service_id)
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            if 'image' in request.FILES:  # Check if image file is included in the request
                service.image = form.cleaned_data['image']
            if 'icon' in request.FILES:  # Check if image file is included in the request
                service.icon = form.cleaned_data['icon']    
            form.save()
            return redirect('app.dashboard.services')
        else:
            return render(request, 'codedictiondashboard/services/edit.html', {
            'form':form,
            'service':service
            })

@method_decorator(staff_member_required, name='dispatch')    
class DeleteServicesViews(CustomLoginRequiredMixin,View):
    def get(self, request, service_id):
        service = get_object_or_404(Services, pk=service_id)
        service.delete()
        result = {
            'status':True
        }
        return JsonResponse(result, safe=False)

@method_decorator(staff_member_required, name='dispatch')    
class StatusServicesViews(CustomLoginRequiredMixin,View):
    def get(self, request, service_id):
        service = get_object_or_404(Services, pk=service_id)
        if service.status == 1:
            service.status=0
        else:
            service.status=1
        service.save()        
        return redirect(request.META.get('HTTP_REFERER'))    
    

    