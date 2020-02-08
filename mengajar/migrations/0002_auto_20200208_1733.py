# Generated by Django 2.2.9 on 2020-02-08 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mengajar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mengajar',
            name='id_guru',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guru.Guru', verbose_name='Guru'),
        ),
        migrations.AlterField(
            model_name='mengajar',
            name='id_mapel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapel.KkmMapel', verbose_name='Mata Pelajaran'),
        ),
    ]
