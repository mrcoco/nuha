from django.db import models

# Create your models here.
class TahunAjaran(models.Model):
    class Meta:
        #app_label = "Tahun Ajaran"
        verbose_name_plural = "Tahun Ajaran"

    PILIH_STATUS = (
        (1,'Aktif'),
        (2,'Non-Aktif')
    )
    tahun = models.CharField(max_length=25)
    status = models.IntegerField(choices=PILIH_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tahun
