from django.contrib import admin

# Register your models here.
from mengajar.models import Mengajar

class MengajarAdmin(admin.ModelAdmin):
    list_display = ['guru','get_mapel']
    def get_mapel(self,obj):
        return "%s - %s - %s" % (obj.mapel.mapel.nama_mapel,obj.mapel.kelas.nama_kelas,obj.mapel.tahun.tahun)
    get_mapel.short_description = 'Mata Pelajaran'

admin.site.register(Mengajar, MengajarAdmin)