from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    return render(request,'index.html')
def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('raport-index')
    else:
        return render(request,'login.html')
def blog(request):
    return render(request,blog.html)