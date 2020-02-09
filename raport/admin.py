from django.contrib import admin

# Register your models here.
from raport.models import Raport


class RaportAdmin(admin.ModelAdmin):
    list_display = ['siswa','tahun','kelas','mapel','pengetahuan','keterampilan']

admin.site.register(Raport, RaportAdmin)