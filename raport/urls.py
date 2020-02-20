from django.urls import path

from .views import KkmCreateView,KkmUpdateView,KkmMapelListView,RaportView,RaportIndexView,RaportDetailView,RaportPrintView,RaportDownloadView,MengajarListView,RaportSiswaView,RaportSiswaDownload,RaportSiswaPrint

urlpatterns = [
    path('',RaportView.as_view(),name="raport-index"),
    path('raport/',RaportIndexView.as_view(),name="raport"),
    path('raport/<int:pk>/detail/',RaportDetailView.as_view(),name="raport-detail"),
    path('raport/<int:pk>/print/', RaportPrintView.as_view(), name="raport-print"),
    path('raport/<int:pk>/download/',RaportDownloadView.as_view(),name="raport-excel"),
    path('raport/<int:siswa>/<int:kelas>/<int:tahun>/detail',RaportSiswaView.as_view(),name='raport-siswa-detail'),
    path('raport/<int:siswa>/<int:kelas>/<int:tahun>/print',RaportSiswaPrint.as_view(),name='raport-siswa-print'),
    path('raport/<int:siswa>/<int:kelas>/<int:tahun>/download',RaportSiswaDownload.as_view(),name='raport-siswa-download'),
    path('mengajar/',MengajarListView.as_view(),name="mengajar"),
    path('kkmmapel/',KkmMapelListView.as_view(),name="kkmmapel"),
    path('kkmmapel/<int:pk>/',KkmUpdateView.as_view(),name="kkm-update"),
    path('kkmmapel/add',KkmCreateView.as_view(),name="kkm-add")
]