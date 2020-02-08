# Generated by Django 2.2.9 on 2020-02-07 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siswa', '0002_auto_20200207_0903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siswa',
            name='agama',
            field=models.IntegerField(choices=[('1', 'Islam'), ('2', 'Katholik'), ('3', 'Kristen'), ('4', 'Hindu'), ('5', 'Budha'), ('6', 'Lainnya')], default=1),
        ),
        migrations.AlterField(
            model_name='siswa',
            name='sex',
            field=models.IntegerField(choices=[('1', 'Laki-Laki'), ('2', 'Perempuan')], default=1),
        ),
    ]
