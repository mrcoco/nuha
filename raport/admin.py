from django.contrib import admin

# Register your models here.
from raport.models import Raport

def get_predikat(kkm, nilai):
    nilaimax = 100
    nilaiKkm = kkm
    interval = (nilaimax - nilaiKkm) / 3
    nilaiA = (nilaimax - interval)
    nilaiB = nilaiA - interval
    nilaiC = nilaiB - interval
    nilaiD = nilaiC - interval
    if nilaiA <= nilai <= nilaimax:
        predikat = "A"
    elif nilaiB <= nilai <= nilaiA:
        predikat = "B"
    elif nilaiC <= nilai <= nilaiB:
        predikat = "C"
    elif nilaiD <= nilai <= nilaiC:
        predikat = "D"
    else:
        predikat = "E"
    return predikat


class RaportAdmin(admin.ModelAdmin):
    list_display = ['siswa','tahun','kelas','mapel','get_kkm_p','pengetahuan','predikat_p','get_kkm_t','keterampilan','predikat_t']

    def get_kkm_p(self,obj):
        return obj.mapel.pengetahuan

    def get_kkm_t(self,obj):
        return obj.mapel.ketrampilan

    def predikat_p(self,obj):
        kkm = obj.mapel.pengetahuan
        nilai = obj.pengetahuan
        predikat = get_predikat(kkm, nilai)
        return predikat

    def predikat_t(self, obj):
        kkm = obj.mapel.ketrampilan
        nilai = obj.keterampilan
        predikat = get_predikat(kkm, nilai)
        return predikat

    get_kkm_p.short_description = "KKM"
    get_kkm_t.short_description = "KKM"
    predikat_p.short_description = "Predikat"
    predikat_t.short_description = "predikat"

admin.site.register(Raport, RaportAdmin)