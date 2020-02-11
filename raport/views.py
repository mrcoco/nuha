from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'raport/index.html')
def kkmmapel(request):
    return render(request,'raport/kkmmapel.html')
def mengajar(request):
    return render(request,'raport/mengajar.html')
def raport(request):
    return render(request,'raport/raport.html')