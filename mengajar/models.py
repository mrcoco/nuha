from django.db import models
from guru.models import Guru
from mapel.models import KkmMapel
from jurusan.models import Kelas
# Create your models here.
class Mengajar(models.Model):
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE, verbose_name="Guru")
    mapel = models.ForeignKey(KkmMapel, on_delete=models.CASCADE, verbose_name="Mata Pelajaran")
    kelas = models.ForeignKey(Kelas,on_delete=models.CASCADE,verbose_name="Kelas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Mengajar"

    def __str__(self):
        nama = self.mapel.mapel.nama_mapel
        kelas = self.mapel.kelas.nama_kelas
        tahun = self.mapel.tahun.tahun

        return "%s - %s - %s" % (nama,kelas,tahun)