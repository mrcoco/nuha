# Generated by Django 2.2.9 on 2020-02-12 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tahunajaran', '0001_initial'),
        ('siswa', '0001_initial'),
        ('jurusan', '0001_initial'),
        ('mapel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Raport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pengetahuan', models.IntegerField(blank=True, null=True)),
                ('keterampilan', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jurusan.Kelas', verbose_name='Kelas')),
                ('mapel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapel.KkmMapel', verbose_name='Mata Pelajaran')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siswa.Siswa')),
                ('tahun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tahunajaran.TahunAjaran', verbose_name='Tahun Ajaran')),
            ],
            options={
                'verbose_name_plural': 'Raport',
            },
        ),
    ]
