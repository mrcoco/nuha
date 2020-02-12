from django.contrib import admin
from mapel.models import Mapel,Mengajar,KkmMapel,DescMapel

# Register your models here.
class InlineMapel(admin.StackedInline):
    model = DescMapel
    extra = 4
    max_num = 4

class MapelAdmin(admin.ModelAdmin):
    list_display = ['nama_mapel']

class MengajarAdmin(admin.ModelAdmin):
    list_display = ['guru','mapel','kelas']

class KkmMapelAdmin(admin.ModelAdmin):
    inlines = [InlineMapel]
    list_display = ['mapel','pengetahuan','ketrampilan']
    list_per_page = 25
admin.site.register(KkmMapel,KkmMapelAdmin)
admin.site.register(Mapel,MapelAdmin)
admin.site.register(Mengajar,MengajarAdmin)
