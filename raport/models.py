from django.db import models

# Create your models here.
from mapel.models import KkmMapel
from siswa.models import Siswa
from tahunajaran.models import TahunAjaran
from jurusan.models import Kelas

class Raport(models.Model):
    siswa = models.ForeignKey(Siswa,on_delete=models.CASCADE)
    tahun = models.ForeignKey(TahunAjaran,on_delete=models.CASCADE,verbose_name="Tahun Ajaran")
    kelas = models.ForeignKey(Kelas,on_delete=models.CASCADE,verbose_name="Kelas")
    mapel = models.ForeignKey(KkmMapel,on_delete=models.CASCADE,verbose_name="Mata Pelajaran")
    pengetahuan = models.IntegerField(blank=True,null=True)
    keterampilan = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Raport"

    def __str__(self):
        return "%s - %s - %s -%s"%(self.siswa,self.tahun.tahun,self.kelas.nama_kelas,self.mapel.mapel.nama_mapel)

