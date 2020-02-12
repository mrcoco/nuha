from django.shortcuts import render,redirect

# Create your views here.
def index(request):
    return render(request,'index.html')
def login(request):
    if request.user.is_authenticated:
        return redirect('raport-index')
    return render(request,'login.html',{"page": login})
def blog(request):
    return render(request,blog.html)