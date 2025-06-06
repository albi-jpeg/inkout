# Generated by Django 5.1.4 on 2025-02-05 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inkoutapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(unique=True)),
                ('hora', models.TimeField()),
                ('artista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='inkoutapp.artista')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to='inkoutapp.usuario')),
            ],
        ),
    ]
