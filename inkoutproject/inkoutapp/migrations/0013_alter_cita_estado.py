# Generated by Django 5.1.4 on 2025-05-27 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inkoutapp', '0012_cita_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='estado',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada'), ('vencida', 'Vencida')], default='pendiente', max_length=10),
        ),
    ]
