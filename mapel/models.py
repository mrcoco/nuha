from django.db import models
from tahunajaran.models import *
from jurusan.models import *

# Create your models here.
class Mapel(models.Model):
    class Meta:
        verbose_name_plural = "Data Mata Pelajaran"
    nama_mapel = models.CharField(max_length=255)
    def __str__(self):
        return self.nama_mapel

class KkmMapel(models.Model):
    class Meta:
        verbose_name_plural = "KKM Mata Pelajaran"
    id_tahun = models.ForeignKey(TahunAjaran,on_delete=models.CASCADE,verbose_name='Tahun Ajaran')
    id_kelas = models.ForeignKey(Kelas,on_delete=models.CASCADE,verbose_name='Kelas')
    id_mapel = models.ForeignKey(Mapel,on_delete=models.CASCADE,verbose_name='Mata Pelajaran')
    pengetahuan = models.IntegerField(blank=True,null=True)
    ketrampilan = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.id_mapel.nama_mapel

class DescMapel(models.Model):
    class Meta:
        verbose_name_plural = "Diskripsi Nilai Mata Pelajaran"
    PILIH_PREDIKAT = (
        ('A', 'A'),
        ('B', 'B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
        ('K','K')
    )
    id_mapel = models.ForeignKey(KkmMapel,on_delete=models.CASCADE)
    predikat = models.CharField(max_length=1,choices=PILIH_PREDIKAT)
    pengetahuan = models.TextField(blank=True,null=True)
    ketrampilan = models.TextField(blank=True,null=True)
    def __str__(self):
        return self.id_mapel.id_mapel.nama_mapel
