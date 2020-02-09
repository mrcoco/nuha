from django.db import models
from guru.models import *
from jurusan.models import *
from tahunajaran.models import *
# Create your models here.
class WaliKelas(models.Model):
    class Meta:
        verbose_name_plural = "Wali Kelas"

    guru = models.ForeignKey(Guru, on_delete=models.CASCADE)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tahun = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)

    def __str__(self):
        return self.kelas.nama_kelas
