# Generated by Django 2.2.9 on 2020-02-08 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mapel', '0004_auto_20200208_0913'),
        ('guru', '0005_auto_20200208_0345'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mengajar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guru.Guru')),
                ('id_mapel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapel.KkmMapel')),
            ],
        ),
    ]
