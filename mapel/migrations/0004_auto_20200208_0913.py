# Generated by Django 2.2.9 on 2020-02-08 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapel', '0003_auto_20200208_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kkmmapel',
            name='id_kelas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jurusan.Kelas', verbose_name='Kelas'),
        ),
        migrations.AlterField(
            model_name='kkmmapel',
            name='id_mapel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapel.Mapel', verbose_name='Mata Pelajaran'),
        ),
        migrations.AlterField(
            model_name='kkmmapel',
            name='id_tahun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tahunajaran.TahunAjaran', verbose_name='Tahun Ajaran'),
        ),
    ]
