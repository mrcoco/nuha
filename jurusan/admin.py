from django.contrib import admin
from jurusan.models import *

# Register your models here.
class InlineKelas(admin.StackedInline):
    model = Kelas
    extra = 3
    max_num = 6

class JurusanAdmin(admin.ModelAdmin):
    inlines = [InlineKelas]
    list_display = ['nama_jurusan']

admin.site.register(Jurusan,JurusanAdmin)