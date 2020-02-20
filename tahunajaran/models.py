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
    PILIH_SEM = (
        (1,'Gasal'),
        (2,'Genap')
    )
    tahun = models.CharField(max_length=25)
    semester = models.IntegerField(choices=PILIH_SEM,default=1)
    status = models.IntegerField(choices=PILIH_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_sem(self):
        if self.semester == 1 :
            sem = "%s (%s)"%(self.semester,"Satu")
        else:
            sem =  "%s (%s)" % (self.semester, "Dua")
        return sem

    def __str__(self):
        if self.semester == 1 :
            sem = "%s (%s)"%(self.semester,"Satu")
        else:
            sem =  "%s (%s)" % (self.semester, "Dua")
        return "%s - %s"%(self.tahun,sem)
