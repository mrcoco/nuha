import os
from os.path import splitext

import uuid
from django.db import models


# Create your models here.
def unique_file_path(instance, filename):
    # Save original file name in model
    instance.original_file_name = filename

    # Get new file name/upload path
    base, ext = splitext(filename)
    newname = "%s%s" % (uuid.uuid4(), ext)
    return os.path.join('web', newname)

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Page(models.Model):

    PILIH_STATUS = (
        (1,'Aktif'),
        (0,'Non-Aktif')
    )
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    intro = models.TextField(max_length=755)
    content = models.TextField()
    image = models.ImageField(upload_to=unique_file_path)
    status = models.IntegerField(choices=PILIH_STATUS)

    def __str__(self):
        return self.title
