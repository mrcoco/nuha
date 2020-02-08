from django.db import models

# Create your models here.
class Mapel(models.Model):
    class Meta:
        verbose_name_plural = "Mata Pelajaran"

    kode_mapel = models.CharField(max_length=25)
    nama_mapel = models.CharField(max_length=255)
    pengetahuan = models.IntegerField()
    ketrampilan = models.IntegerField()

    def __str__(self):
        return self.nama_mapel

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
    id_mapel = models.ForeignKey(Mapel,on_delete=models.CASCADE)
    predikat = models.CharField(max_length=1,choices=PILIH_PREDIKAT)
    pengetahuan = models.TextField()
    ketrampilan = models.TextField()

    def __str__(self):
        return self.id_mapel.nama_mapel
