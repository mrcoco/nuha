from django.contrib import admin
from mapel.models import *

# Register your models here.
class InlineMapel(admin.StackedInline):
    model = DescMapel
    extra = 4
    max_num = 4
class MapelAdmin(admin.ModelAdmin):
    list_display = ['nama_mapel']

class KkmMapelAdmin(admin.ModelAdmin):
    inlines = [InlineMapel]
    list_display = ['id_mapel','pengetahuan','ketrampilan']
    #list_filter = ('nama_mapel', 'pengetahuan', 'ketrampilan')
    #search_fields = ['nama_mapel', 'pengetahuan', 'ketrampilan']
    list_per_page = 25
admin.site.register(KkmMapel,KkmMapelAdmin)
admin.site.register(Mapel,MapelAdmin)
#class DescAdmin(admin.ModelAdmin):
    #list_display = ['get_mapel','predikat', 'pengetahuan', 'ketrampilan']
    # list_filter = ('nama_mapel','predikat', 'pengetahuan', 'ketrampilan')
    #search_fields = ['get_mapel','predikat','pengetahuan', 'ketrampilan']
    #list_per_page = 25
    #def get_mapel(self,obj):
        #return obj.id_mapel.nama_mapel

#admin.site.register(DescMapel,DescAdmin)
