from django.db import models
from guru.models import Guru
from mapel.models import KkmMapel
# Create your models here.
class Mengajar(models.Model):
    id_guru = models.ForeignKey(Guru,on_delete=models.CASCADE,verbose_name="Guru")
    id_mapel = models.ForeignKey(KkmMapel,on_delete=models.CASCADE,verbose_name="Mata Pelajaran")

    class Meta:
        verbose_name_plural = "Mengajar"

    def __str__(self):
        nama = self.id_mapel.id_mapel.nama_mapel
        kelas = self.id_mapel.id_kelas.nama_kelas
        tahun = self.id_mapel.id_tahun.tahun

        return "%s - %s - %s" % (nama,kelas,tahun)