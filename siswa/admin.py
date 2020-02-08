from django.contrib import admin
from django.utils.html import format_html

from siswa.models import *
# Register your models here.
class SiswaAdmin(admin.ModelAdmin):
    def get_foto(self,obj):
        return format_html('<img src="{}" width="100" height="100"/>'.format(obj.foto.url))

    get_foto.short_description = 'Image'
    list_display = ['nama', 'get_foto','nisn', 'alamat_ayah','nama_ayah','nama_ibu']
    # list_filter = ('nama_mapel', 'pengetahuan', 'ketrampilan')
    search_fields = ['nama', 'nisn', 'alamat_ayah','nama_ayah','nama_ibu']
    list_per_page = 25

admin.site.register(Siswa, SiswaAdmin)