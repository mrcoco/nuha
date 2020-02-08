# Generated by Django 2.2.9 on 2020-02-07 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jurusan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_jurusan', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Kelas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_kelas', models.CharField(max_length=255)),
                ('id_jurusan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jurusan.Jurusan')),
            ],
        ),
    ]
