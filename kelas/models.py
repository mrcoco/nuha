from django.db import models
from jurusan.models import *
from siswa.models import *
# Create your models here.
class Kelas(models.Model):
    id_kelas = models.ForeignKey(Kelas,on_delete=models.CASCADE)
    id_siswa = models.ForeignKey(Siswa,on_delete=models.CASCADE)
    def __str__(self):
        return self.id_siswa.nama
