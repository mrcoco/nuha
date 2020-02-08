from django.contrib import admin
from kelas.models import *

#class InlineSiswa(admin.StackedInline):
#    model = Siswa

class KelasAdmin(admin.ModelAdmin):
    #inlines = [InlineSiswa]
    list_display = ['get_siswa','id_kelas']
    #list_display = ['nama','nisn']
    #list_filter = ['id_siswa']
    def get_siswa(self,obj):
        return obj.id_siswa.nama
    #def get_kelas(self,obj):
    #    return obj.id_kelas.nama_kelas
#.site.register(Siswa)
admin.site.register(Kelas, KelasAdmin)
