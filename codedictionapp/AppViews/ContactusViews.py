import math
import datetime
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views import View
from codedictionapp.models import Contactus
from codedictionapp.forms import ContactusForm
    
@method_decorator(csrf_exempt, name="dispatch") 
class AddContactusViews(View):

    # def get(self, request):
    #     return render(request, 'codedictiondashboard/blog/add.html')    
    
    @method_decorator(csrf_protect)
    def post(self, request):
        form = ContactusForm(request.POST)
        if form.is_valid():
            form.save()
            url = request.META.get('HTTP_REFERER') # Assuming 'my_redirected_view' is the name of the target view
            form = "Success"
            return redirect('{}?form={}'.format(url, form))
        else:
            return render(request, 'courses/contact.html', {
                'form':form
            })  