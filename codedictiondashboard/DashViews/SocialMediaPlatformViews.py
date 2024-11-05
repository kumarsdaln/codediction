from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from codedictionapp.models import SocialMediaPlatform
from codedictiondashboard.forms import SocialMediaPlatformForm

class SocialMediaPlatformManageView(View):
    template_name = 'codedictiondashboard/social-media-platform/manage.html'

    def get(self, request, platform_id=None):
        if platform_id:
            platform = get_object_or_404(SocialMediaPlatform, id=platform_id)
        else:
            platform = None

        platforms = SocialMediaPlatform.objects.all()
        form = SocialMediaPlatformForm(instance=platform)
        return render(request, self.template_name, {
            'platforms': platforms,
            'form': form,
            'platform': platform
        })

    def post(self, request, platform_id=None):
        if 'delete' in request.POST:
            platform = get_object_or_404(SocialMediaPlatform, id=platform_id)
            platform.delete()
            return redirect('app.dashboard.social-media-platform')
        
        if platform_id:
            platform = get_object_or_404(SocialMediaPlatform, id=platform_id)
            form = SocialMediaPlatformForm(request.POST, instance=platform)
        else:
            form = SocialMediaPlatformForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('app.dashboard.social-media-platform')

        platforms = SocialMediaPlatform.objects.all()
        return render(request, self.template_name, {
            'platforms': platforms,
            'form': form,
            'platform': platform
        })
