from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from codedictionapp.models import BlogCategory, Blog
from django.core.paginator import Paginator
import math
import readtime
import datetime
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictiondashboard.forms import BlogForm


class BlogViews(CustomLoginRequiredMixin,ListView):
    paginate_by = 10
    model = Blog
    template_name = 'codedictiondashboard/blog/index.html'
    context_object_name = 'blog_list'
    queryset = Blog.objects.order_by('-uploaded_at')
    def get(self, request, *args, **kwargs):
        current_page = request.GET.get('page', 1)
        total_pages = self.get_paginator(self.queryset, self.paginate_by).num_pages
        if int(current_page) > int(total_pages):
            return redirect(f'{self.request.path}?page={total_pages}')
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_blog"] = Blog.objects.count()
        return context

class BlogByCategoryView(CustomLoginRequiredMixin,ListView):
    model = Blog
    template_name = 'codedictiondashboard/blog/index.html'
    context_object_name = 'blog_list'
    paginate_by = 10
    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        return Blog.objects.filter(category__slug=category_slug)
    def get(self, request, *args, **kwargs):
        current_page = request.GET.get('page', 1)
        total_pages = self.get_paginator(self.get_queryset(), self.paginate_by).num_pages
        if int(current_page) > int(total_pages):
            return redirect(f'{self.request.path}?page={total_pages}')
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['category_slug']
        context['current_category'] = BlogCategory.objects.get(slug=category_slug)
        context["total_blog"] = Blog.objects.filter(category__slug=category_slug).count()
        return context  

class BlogByStatusView(CustomLoginRequiredMixin,ListView):
    model = Blog
    template_name = 'codedictiondashboard/blog/index.html'
    context_object_name = 'blog_list'
    paginate_by = 10

    def get_queryset(self):
        # Get the category slug from the URL parameters
        status = self.kwargs['status']
        if status == 'active':
            status=1
        else:  
            status=0  
        
        # Filter blogs by the specified category
        return Blog.objects.filter(status=status)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the original context
        context = super().get_context_data(**kwargs)
        return context  
    
class BlogDetailViews(CustomLoginRequiredMixin,DetailView):
    model = Blog
    template_name = 'codedictiondashboard/blog/view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context    
    
@method_decorator(csrf_exempt, name="dispatch") 
class AddBlogViews(CustomLoginRequiredMixin,View):

    def get(self, request):
        blog_categories = BlogCategory.objects.all()
        return render(request, 'codedictiondashboard/blog/add.html', {
            'blog_categories':blog_categories
        })    
    
    @method_decorator(csrf_protect)
    def post(self, request):
        blog_categories = BlogCategory.objects.all()
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user,uploaded_at=True)
            return redirect('app.dashboard.blog')
        else:
            return render(request,'codedictiondashboard/blog/add.html', {
                'form':form,
                'blog_categories':blog_categories
            })
    
@method_decorator(csrf_exempt, name="dispatch") 
class EditBlogViews(CustomLoginRequiredMixin,View):

    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        blog_categories = BlogCategory.objects.all()
        form = BlogForm(instance=blog)
        return render(request, 'codedictiondashboard/blog/edit.html', {
            'blog':blog,
            'blog_categories':blog_categories,
            'form':form
        })    
    
    @method_decorator(csrf_protect)
    def post(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        blog_categories = BlogCategory.objects.all()
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            if 'image' in request.FILES:
                blog.image = form.cleaned_data['image']
            form.save()
            return redirect('app.dashboard.blog')
        else:
            return render(request,'codedictiondashboard/blog/edit.html', {
                'form':form,
                'blog_categories':blog_categories,
                'blog':blog
            })
    
class DeleteBlogViews(CustomLoginRequiredMixin,View):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        blog.delete()
        result = {
            'status':True
        }
        return JsonResponse(result, safe=False)
    
class StatusBlogViews(CustomLoginRequiredMixin,View):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        if blog.status == 1:
            blog.status=0
        else:
            blog.status=1
        blog.save()        
        return redirect(request.META.get('HTTP_REFERER'))    
    

    