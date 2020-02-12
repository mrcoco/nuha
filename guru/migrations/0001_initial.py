# Generated by Django 2.2.9 on 2020-02-12 04:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guru',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('nip', models.CharField(max_length=50)),
                ('sex', models.IntegerField(choices=[(1, 'Laki-Laki'), (2, 'Perempuan')])),
                ('agama', models.IntegerField(choices=[(1, 'Islam'), (2, 'Katholik'), (3, 'Kristen'), (4, 'Hindu'), (5, 'Budha'), (6, 'Lainnya')])),
                ('alamat', models.TextField()),
                ('foto', models.ImageField(blank=True, null=True, upload_to='guru/')),
                ('tmp_lahir', models.CharField(max_length=100)),
                ('tgl_lahir', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guru', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Guru',
            },
        ),
    ]
