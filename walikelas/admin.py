from django.contrib import admin
from walikelas.models import WaliKelas
from guru.models import Guru

# Register your models here.
class WaliKelasAdmin(admin.ModelAdmin):
    list_display = ['get_guru','get_kelas','get_tahun']
    def get_guru(self,obj):
        return obj.guru.nama
    def get_kelas(self,obj):
        return obj.kelas.nama_kelas
    def get_tahun(self,obj):
        return obj.tahun.tahun
    @staticmethod
    def autocomplete_search_fields():
        return 'guru__nama', 'kelas__nama_kelas','tahun__tahun'
    get_guru.short_description = "Guru"
    get_kelas.short_description = "Kelas"
    get_tahun.short_description = "Tahun Ajaran"
admin.site.register(WaliKelas, WaliKelasAdmin)