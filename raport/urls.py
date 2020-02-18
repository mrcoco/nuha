from django.urls import path
from django.contrib import admin
from . import views
from .views import KkmCreateView,KkmUpdateView,KkmMapelListView,RaportIndexView,RaportDetailView,RaportPrintView,RaportDownloadView,MengajarListView

admin.site.site_header = "SIAKAD NUHA Admin"
admin.site.site_title = "SIAKAD NUHA Admin Portal"
admin.site.index_title = "Sistem Informasi Akademik - SMK Ma'arif Nurul Haromain"

urlpatterns = [
    path('',views.index,name="raport-index"),
    path('raport/',RaportIndexView.as_view(),name="raport"),
    path('raport/<int:pk>/detail/',RaportDetailView.as_view(),name="raport-detail"),
    path('raport/<int:pk>/print/', RaportPrintView.as_view(), name="raport-print"),
    path('raport/<int:pk>/download/',RaportDownloadView.as_view(),name="raport-excel"),
    path('mengajar/',MengajarListView.as_view(),name="mengajar"),
    path('kkmmapel/',KkmMapelListView.as_view(),name="kkmmapel"),
    path('kkmmapel/<int:pk>/',KkmUpdateView.as_view(),name="kkm-update"),
    path('kkmmapel/add',KkmCreateView.as_view(),name="kkm-add")
]