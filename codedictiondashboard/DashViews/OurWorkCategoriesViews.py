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
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictionapp.models import WorkCategories
from codedictiondashboard.forms import WorkCategoriesForm

class BlogCategoryViews(CustomLoginRequiredMixin,ListView):
    model = BlogCategory
    template_name = 'codedictiondashboard/blog/category/index.html'
    queryset = BlogCategory.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
@method_decorator(csrf_exempt, name="dispatch") 
class AddBlogCategoryViews(CustomLoginRequiredMixin,View):   
    
    @method_decorator(csrf_protect)
    def post(self, request):
        form = BlogCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return render(request, 'codedictiondashboard/blog/category/index.html', {
                'form':form
            })  
    
@method_decorator(csrf_exempt, name="dispatch") 
class EditBlogCategoryViews(CustomLoginRequiredMixin,View):  
    
    @method_decorator(csrf_protect)
    def post(self, request, category_id):
        category = get_object_or_404(BlogCategory, pk=category_id)
        category.name=request.POST.get('name')
        category.slug=request.POST.get('slug')
        category.meta_tags=request.POST.get('meta_tags')
        category.save()
        return redirect('app.dashboard.blog.category')    
    
class DeleteBlogCategoryViews(CustomLoginRequiredMixin,View):
    def get(self, request, category_id):
        category = get_object_or_404(BlogCategory, pk=category_id)
        category.delete()
        result = {
            'status':True
        }
        return JsonResponse(result, safe=False)  