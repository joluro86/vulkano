from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.shortcuts import render, redirect

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

def landing_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')
