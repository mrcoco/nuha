from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login

# Create your views here.
from django.urls import reverse
from django.views.generic import TemplateView


class FrontEndIndex(TemplateView):
    template_name = 'frontend/home.html'

class LoginView(TemplateView):
    template_name = 'frontend/login_page.html'
    def post(self,request,**kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('raport-index'))
            else:
                return render(request, self.template_name)
