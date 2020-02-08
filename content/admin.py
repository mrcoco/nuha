from django.contrib import admin
from content.models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class ContenAdmin(admin.ModelAdmin):
    list_display = ['title','image','intro']

admin.site.register(Content, ContenAdmin)
admin.site.register(Category,CategoryAdmin)