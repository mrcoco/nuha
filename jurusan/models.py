from django.db import models

# Create your models here.
class Jurusan(models.Model):
    class Meta:
        verbose_name_plural = "Daftar Jurusan"

    nama_jurusan = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_jurusan

class Kelas(models.Model):
    class Meta:
        verbose_name_plural = "Daftar Kelas"
    jurusan = models.ForeignKey(Jurusan, on_delete=models.CASCADE)
    nama_kelas = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama_kelas