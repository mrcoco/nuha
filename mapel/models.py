from django.db import models
from tahunajaran.models import TahunAjaran
from jurusan.models import Jurusan,Kelas
from guru.models import Guru

# Create your models here.
class Mapel(models.Model):
    class Meta:
        verbose_name_plural = "Data Mata Pelajaran"

    nama_mapel = models.CharField(max_length=255,verbose_name="Mata Pelajaran")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_mapel

class Mengajar(models.Model):
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE, verbose_name="Guru")
    mapel = models.ForeignKey(Mapel, on_delete=models.CASCADE, verbose_name="Mata Pelajaran")
    kelas = models.ForeignKey(Kelas,on_delete=models.CASCADE,verbose_name="Kelas")
    tahun = models.ForeignKey(TahunAjaran,on_delete=models.CASCADE,verbose_name="Tahun Ajaran",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Jadwal Mengajar"

    def __str__(self):
        nama = self.mapel.nama_mapel
        kelas = self.kelas.nama_kelas
        tahun = self.tahun.tahun

        return "%s - %s - %s" % (nama,kelas,tahun)

class KkmMapel(models.Model):
    class Meta:
        verbose_name_plural = "KKM Mata Pelajaran"

    tahun = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE, verbose_name='Tahun Ajaran')
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, verbose_name='Kelas')
    mapel = models.OneToOneField(Mengajar, on_delete=models.CASCADE,unique=True, verbose_name='Mata Pelajaran')
    pengetahuan = models.IntegerField(blank=True,null=True)
    ketrampilan = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s - %s"%(self.mapel.mapel.nama_mapel, self.kelas.nama_kelas, self.tahun.tahun)

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
    mapel = models.ForeignKey(KkmMapel, on_delete=models.CASCADE)
    predikat = models.CharField(max_length=1,choices=PILIH_PREDIKAT)
    pengetahuan = models.TextField(blank=True,null=True)
    ketrampilan = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mapel.mapel.mapel.nama_mapel
