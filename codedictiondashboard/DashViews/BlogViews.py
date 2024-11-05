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
from django.views.generic.detail import DetailView
from codedictionapp.models import BlogCategory, Blog
from codedictiondashboard.CustomLoginRequiredMixin import CustomLoginRequiredMixin
from codedictiondashboard.forms import BlogForm
from django.db.models import Q

@method_decorator(staff_member_required, name='dispatch')
class BlogViews(CustomLoginRequiredMixin,ListView):
    paginate_by = 10
    model = Blog
    template_name = 'codedictiondashboard/blog/index.html'
    context_object_name = 'blog_list'
    def get_queryset(self):
        queryset = Blog.objects.all()

        # Filtering by status (active/inactive)
        status = self.request.GET.get('status', None)
        if status is not None:
            if status == 'active':
                queryset = queryset.filter(status=True)
            elif status == 'inactive':
                queryset = queryset.filter(status=False)
        # Searching
        search = self.request.GET.get('q', None)
        if search is not None:
            search = search.strip()
            queryset = queryset.filter(
                Q(category__name__icontains=search) | 
                Q(title__icontains=search) | 
                Q(brief__icontains=search) |
                Q(description__icontains=search)
            ).distinct()
        # Sorting by 'id' or 'title' with direction
        sort_by = self.request.GET.get('sort_by', 'uploaded_at')
        sort_direction = self.request.GET.get('sort_direction', 'desc')

        if sort_by in ['id', 'title', 'uploaded_at']:
            if sort_direction == 'asc':
                queryset = queryset.order_by(sort_by)
            else:
                queryset = queryset.order_by(f'-{sort_by}')

        return queryset
    def get(self, request, *args, **kwargs):
        current_page = request.GET.get('page', 1)
        total_pages = self.get_paginator(self.get_queryset(), self.paginate_by).num_pages
        if int(current_page) > int(total_pages):
            return redirect(f'{self.request.path}?page={total_pages}')
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_blog"] = self.get_queryset().count()
        context['q'] = self.request.GET.get('q', None)
        return context
    
@method_decorator(staff_member_required, name='dispatch')    
class BlogDetailViews(CustomLoginRequiredMixin,DetailView):
    model = Blog
    template_name = 'codedictiondashboard/blog/view.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context    
    
@method_decorator([csrf_exempt, staff_member_required], name="dispatch") 
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
    
@method_decorator([csrf_exempt, staff_member_required], name="dispatch") 
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
        
@method_decorator(staff_member_required, name='dispatch')    
class DeleteBlogViews(CustomLoginRequiredMixin,View):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        blog.delete()
        result = {
            'status':True
        }
        return JsonResponse(result, safe=False)
    
@method_decorator(staff_member_required, name='dispatch')    
class StatusBlogViews(CustomLoginRequiredMixin,View):
    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        if blog.status == 1:
            blog.status=0
        else:
            blog.status=1
        blog.save()        
        return redirect(request.META.get('HTTP_REFERER'))    
    

    