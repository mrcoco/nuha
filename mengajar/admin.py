from django.contrib import admin

# Register your models here.
from mengajar.models import Mengajar

class MengajarAdmin(admin.ModelAdmin):
    list_display = ['id_guru','get_mapel']
    def get_mapel(self,obj):
        return "%s - %s - %s" % (obj.id_mapel.id_mapel.nama_mapel,obj.id_mapel.id_kelas.nama_kelas,obj.id_mapel.id_tahun.tahun)
    get_mapel.short_description = 'Mata Pelajaran'

admin.site.register(Mengajar, MengajarAdmin)