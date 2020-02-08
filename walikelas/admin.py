from django.contrib import admin
from walikelas.models import *
from guru.models import *

# Register your models here.
class WaliKelasAdmin(admin.ModelAdmin):
    list_display = ['get_guru','get_kelas','get_tahun']
    def get_guru(self,obj):
        return obj.id_guru.nama
    def get_kelas(self,obj):
        return obj.id_kelas.nama_kelas
    def get_tahun(self,obj):
        return obj.id_tahun.tahun
admin.site.register(WaliKelas, WaliKelasAdmin)