from django.contrib import admin
from tahunajaran.models import *
# Register your models here.
class TahunAjaranAdmin(admin.ModelAdmin):
    list_display = ['tahun','status']
admin.site.register(TahunAjaran,TahunAjaranAdmin)