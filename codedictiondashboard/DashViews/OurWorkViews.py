from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from codedictionapp.models import OurWork

class OurWorkListView(ListView):
    model = OurWork
    template_name = 'ourwork_list.html'
    context_object_name = 'works'

class OurWorkDetailView(DetailView):
    model = OurWork
    template_name = 'ourwork_detail.html'
    context_object_name = 'work'

class OurWorkCreateView(CreateView):
    model = OurWork
    fields = ['name', 'image', 'description', 'slug', 'work_category', 'meta_data']
    template_name = 'ourwork_form.html'
    success_url = reverse_lazy('ourwork_list')

class OurWorkUpdateView(UpdateView):
    model = OurWork
    fields = ['name', 'image', 'description', 'slug', 'work_category', 'meta_data']
    template_name = 'ourwork_form.html'
    success_url = reverse_lazy('ourwork_list')

class OurWorkDeleteView(DeleteView):
    model = OurWork
    template_name = 'ourwork_confirm_delete.html'
    success_url = reverse_lazy('ourwork_list')
