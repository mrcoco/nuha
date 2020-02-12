from django.contrib import admin
from django.utils.html import format_html
from guru.models import Guru
# Register your models here.
class GuruAdmin(admin.ModelAdmin):

    def get_foto(self,obj):
        return format_html('<img src="{}" width="100" height="100"/>'.format(obj.foto.url))

    get_foto.short_description = 'Foto'
    list_display = ['nama','get_foto',  'nip', 'alamat']
    # list_filter = ('nama_mapel', 'pengetahuan', 'ketrampilan')
    search_fields = ['nama', 'nip', 'alamat']
    list_per_page = 25
admin.site.register(Guru, GuruAdmin)