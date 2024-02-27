from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views import View

@method_decorator(csrf_exempt, name="dispatch") 
class LoginViews(View):
    def get(self,request):
        redirect_url = request.GET.get('next', 'app.dashboard')
        return render(request, 'codedictiondashboard/auth/login.html', {
            'redirect_url':redirect_url
        })
    @method_decorator(csrf_protect)
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        redirect_url = request.POST.get('redirect_url', 'app.dashboard')
        print(redirect_url)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(redirect_url)
        else:
            return render(request, 'codedictiondashboard/auth/login.html', {'error': 'Invalid username or password'})
        
class LogoutViews(View):
    def get(self,request):
        logout(request)
        return redirect('app.dashboard.login')          