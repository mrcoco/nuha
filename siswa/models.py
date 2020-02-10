import os
from os.path import splitext

import uuid
from django.db import models
from django.db.models.fields.files import *
from jurusan.models import *
from tahunajaran.models import *
from django.conf import settings

def unique_file_path(instance, filename):
    # Save original file name in model
    instance.original_file_name = filename

    # Get new file name/upload path
    base, ext = splitext(filename)
    newname = "%s%s" % (uuid.uuid4(), ext)
    return os.path.join('siswa', newname)

# Create your models here.
class Siswa(models.Model):
    class Meta:
        verbose_name_plural = "Siswa"
    PILIH_SEX = (
        (1, 'Laki-Laki'),
        (2, 'Perempuan')
    )
    PILIH_AGAMA = (
        (1, 'Islam'),
        (2, 'Katholik'),
        (3, 'Kristen'),
        (4, 'Hindu'),
        (5, 'Budha'),
        (6, 'Lainnya')
    )
    nama = models.CharField(max_length=255)
    nis = models.CharField(max_length=50,verbose_name='NIS')
    nisn = models.CharField(max_length=50,verbose_name='NISN')
    sex = models.IntegerField(default=1,choices=PILIH_SEX,verbose_name='Jenis Kelamin')
    agama = models.IntegerField(default=1,choices=PILIH_AGAMA)
    tmp_lahir = models.CharField(max_length=100, null=True, blank=True,verbose_name='Tempat Lahir')
    tgl_lahir = models.DateField(null=True, blank=True,verbose_name='Tanggal Lahir')
    #foto = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT, "upload/siswa"), blank=True)
    foto = models.ImageField(upload_to=unique_file_path)
    nama_ayah = models.CharField(max_length=150)
    nama_ibu = models.CharField(max_length=150)
    pekerjaan_ayah = models.CharField(max_length=150)
    pekerjaan_ibu = models.CharField(max_length=150)
    alamat_ayah = models.TextField()
    telp_ayah = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

class Kelas(models.Model):
    class Meta:
        verbose_name_plural = "Data Kelas"
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    tahun = models.ForeignKey(TahunAjaran, on_delete=models.CASCADE)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.siswa.nama