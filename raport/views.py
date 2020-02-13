from django.shortcuts import render,redirect
from guru.models import Guru
from mapel.models import KkmMapel,Kelas,Mapel,DescMapel,Mengajar


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {

    }
    return render(request,'raport/index.html',context)

def kkmmapel(request):
    guru  = get_guru(request.user.id)
    jadwal = get_mengajar(guru)
    context = {
        'guru': guru,
        'jadwal': jadwal
    }
    return render(request,'raport/kkmmapel.html',context)

def kkmadd(request):
    pass

def kkmupdate(request):
    pass

def get_kkm(id):
    return KkmMapel.objects.filter(mapel_id=id)

def get_mengajar(guru):
    return Mengajar.objects.filter(guru_id=guru.id)

def mengajar(request):
    guru = get_guru(request.user.id)
    jadwal = get_mengajar(guru)
    context = {
        'jadwal': jadwal,
        'guru': guru
    }
    return render(request,'raport/mengajar.html',context)

def raport(request):
    return render(request,'raport/raport.html')

def get_guru(userid):
    return Guru.objects.get(user=userid)