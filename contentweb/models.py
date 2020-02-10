import os
from os.path import splitext

import uuid
from django.db import models


# Create your models here.
def unique_file_path(instance, filename):
    return unique_file(instance, filename,'web')

def unique_slider_path(instance, filename):
    return unique_file(instance, filename, 'banner')

def unique_gallery_path(instance, filename):
    return unique_file(instance, filename, 'gallery')

def unique_file(instance, filename,mypath):
    # Save original file name in model
    instance.original_file_name = filename

    # Get new file name/upload path
    base, ext = splitext(filename)
    newname = "%s%s" % (uuid.uuid4(), ext)
    return os.path.join(mypath, newname)

#class TimeStampMixin(models.Model):
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now=True)
#
#    class Meta:
#        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Category"
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Page"

    def __str__(self):
        return self.title

class Slider(models.Model):
    image = models.ImageField(upload_to=unique_slider_path,unique=True)
    title = models.CharField(max_length=255)
    link  = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Slider"

    def __str__(self):
        return self.title

class GalleryCategory(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Gallery Category"
    def __str__(self):
        return self.name

class Gallery(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=unique_gallery_path)
    category = models.ForeignKey(GalleryCategory,on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Gallery"
    def __str__(self):
        return self.title

class Contact(models.Model):
    name  = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Contact"

    def __str__(self):
        return self.name