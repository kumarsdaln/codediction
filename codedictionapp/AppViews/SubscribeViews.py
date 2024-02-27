import math
import datetime
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views import View
from codedictionapp.models import SubscribeNewsletter
from codedictionapp.forms import SubscribeNewsletterForm
    
@method_decorator(csrf_exempt, name="dispatch") 
class AddSubscribeViews(View):

    # def get(self, request):
    #     return render(request, 'codedictiondashboard/blog/add.html')    
    
    @method_decorator(csrf_protect)
    def post(self, request):
        form = SubscribeNewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            url = request.META.get('HTTP_REFERER') # Assuming 'my_redirected_view' is the name of the target view
            result = {
                'status':True
            }
           
        else:
            result = {
                'status':False
            }

        return JsonResponse(result, safe=False)  