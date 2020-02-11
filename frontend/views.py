from django.shortcuts import render,redirect

# Create your views here.
def index(request):
    return render(request,'index.html')
def login(request):

    #try:
    #    if request.session['userid']:
    #        return redirect('raport')
    #except:
    #    pass
    return render(request,'login.html',{"page": login})
def blog(request):
    return render(request,blog.html)