from django.urls import path
from django.contrib import admin
from . import views
from .views import KkmCreateView

admin.site.site_header = "SIAKAD NUHA Admin"
admin.site.site_title = "SIAKAD NUHA Admin Portal"
admin.site.index_title = "Sistem Informasi Akademik - SMK Ma'arif Nurul Haromain"

urlpatterns = [
    path('',views.index,name="raport-index"),
    path('raport/',views.raport,name="raport"),
    path('mengajar/',views.mengajar,name="mengajar"),
    path('kkmmapel/',views.kkmmapel,name="kkmmapel"),
    path('kkmapel/<int:id>/change',views.kkmupdate,name="kkm-update"),
    path('kkmmapel/add',KkmCreateView.as_view(),name="kkm-add")
]