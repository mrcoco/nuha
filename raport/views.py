from django.shortcuts import render
from guru.models import Guru
from mapel.models import KkmMapel,Kelas,Mapel,DescMapel
#from mengajar.models import Mengajar



# Create your views here.
def index(request):
    return render(request,'raport/index.html')
# def index(request):
#     guru = get_guru(request.user.id)
#     mengajar = Mengajar.objects.filter(guru=guru.id)
#     #kkm = KkmMapel.objects.get(mapel=mengajar.mapel)
#     context = {
#         #'kkm': kkm,
#         'iduser': request.user.id,
#         'mengajar': mengajar,
#         'userguru': guru.nama
#     }
#     return render(request,'raport/index.html',context)
#
# def kkmmapel(request):
#     guru  = get_guru(request.user.id)
#     mapel = Mapel.objects.all()
#     mengajar = get_mengajar(guru)
#     kkm = get_kkm(mengajar)
#     context = {
#         'mapel': mapel,
#         'mengajar': mengajar,
#         'kkm': kkm,
#         'guru': guru,
#     }
#     return render(request,'raport/kkmmapel.html',context)
#
#
# def get_kkm(mengajar):
#     return KkmMapel.objects.filter(mapel=mengajar.mapel_id)
#
#
# def get_mengajar(guru):
#     return Mengajar.objects.filter(guru=guru.id)
#
#
# def mengajar(request):
#     return render(request,'raport/mengajar.html')
# def raport(request):
#     return render(request,'raport/raport.html')
#
# def get_guru(userid):
#     return Guru.objects.get(user=userid)