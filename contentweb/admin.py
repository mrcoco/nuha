from django.contrib import admin
from django.utils.html import format_html
from contentweb.models import Page,Category
# Register your models here.
class PageWebAdmin(admin.ModelAdmin):
    list_display = ['title','get_image','category','intro']
    def get_image(self,obj):
        return format_html('<img src="{}" width="100" height="100"/>'.format(obj.image.url))
    get_image.short_description = 'Banner'
admin.site.register(Page, PageWebAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Category, CategoryAdmin)