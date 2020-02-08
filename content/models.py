from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Content(models.Model):
    PILIH_STATUS = (
        (1,'Aktif'),
        (0,'Non-Aktif')
    )
    id_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    intro = models.CharField(max_length=700)
    content = models.TextField()
    image = models.ImageField(upload_to='content/')
    status = models.IntegerField(choices=PILIH_STATUS)

    def __str__(self):
        return self.title