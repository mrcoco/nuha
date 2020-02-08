from django.db import models

# Create your models here.
class Guru(models.Model):
    class Meta:
        verbose_name_plural = "Guru"
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
    nip = models.CharField(max_length=50)
    sex = models.IntegerField(choices=PILIH_SEX)
    agama = models.IntegerField(choices=PILIH_AGAMA)
    alamat = models.TextField()
    foto = models.ImageField(upload_to='guru/',blank=True,null=True)
    tmp_lahir = models.CharField(max_length=100)
    tgl_lahir = models.DateField()

    def __str__(self):
        return self.nama