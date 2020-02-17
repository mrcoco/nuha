from functools import partial

from django.contrib import admin
from django.forms import ModelForm

from mapel.models import Mapel,Mengajar,KkmMapel,DescMapel
from raport.models import Raport
from siswa.models import Siswa,Kelas

# Register your models here.
class RaportlineForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super(RaportlineForm, self).__init__(*args, **kwargs)
    self.fields['siswa'].queryset = Siswa.objects.filter(kelas__kelas__kkmmapel=11)

class InlineMapel(admin.StackedInline):
    model = DescMapel
    extra = 4
    max_num = 4

class InlineRaport(admin.TabularInline):
    form = RaportlineForm
    model = Raport
    # def get_form(self, request, obj=None, **kwargs):
    #     if request.user.is_superuser:
    #         pass
    #     else:
    #         kwargs['formfield_callback'] = partial(self.formfield_for_dbfield, request=request)
    #     return super(InlineRaport, self).get_form(request, obj, **kwargs)
    #
    # def formfield_for_dbfield(self, db_field, **kwargs):
    #     field = super(InlineRaport, self).formfield_for_dbfield(db_field, **kwargs)
    #     if db_field.name == 'siswa':
    #         field.queryset = field.queryset.filter(kelas__kelas__in=1)
    #     return field

class MapelAdmin(admin.ModelAdmin):
    list_display = ['nama_mapel']

class MengajarAdmin(admin.ModelAdmin):
    list_display = ['guru','mapel','kelas']

class KkmMapelAdmin(admin.ModelAdmin):
    inlines = [InlineMapel,InlineRaport]
    list_display = ['mapel','pengetahuan','ketrampilan']
    list_per_page = 25
admin.site.register(KkmMapel,KkmMapelAdmin)
admin.site.register(Mapel,MapelAdmin)
admin.site.register(Mengajar,MengajarAdmin)
