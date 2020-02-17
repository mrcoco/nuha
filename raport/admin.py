from functools import partial

from django.contrib import admin

# Register your models here.
from raport.models import Raport
from siswa.models import Siswa

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
    list_display = ['siswa','mapel','get_kkm_p','pengetahuan','predikat_p','get_kkm_t','keterampilan','predikat_t']

    def get_form(self, request, obj=None, **kwargs):
        kwargs['formfield_callback'] = partial(self.formfield_for_dbfield, request=request)
        return super(RaportAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(RaportAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'siswa':
            field.queryset = field.queryset.filter(kelas__kelas__kkmmapel=11)
        return field

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