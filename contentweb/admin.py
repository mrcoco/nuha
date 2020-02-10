from django.contrib import admin
from django.utils.html import format_html
from contentweb.models import Page,Category,Slider,Gallery,GalleryCategory,Contact
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

class SliderAdmin(admin.ModelAdmin):
    list_display = ['title','get_image','link']
    def get_image(self,obj):
        return format_html('<img src="{}" width="100" height="100"/>'.format(obj.image.url))
    get_image.short_description = 'Banner'
admin.site.register(Slider,SliderAdmin)

class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(GalleryCategory,GalleryCategoryAdmin)

class GalleryAdmin(admin.ModelAdmin):
    #inlines = [InlineGalleryCategory]
    list_display = ['title','get_image','category']
    def get_image(self,obj):
        return format_html('<img src="{}" width="100" height="100"/>'.format(obj.image.url))
    get_image.short_description = 'Image'
admin.site.register(Gallery,GalleryAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','message']
admin.site.register(Contact,ContactAdmin)