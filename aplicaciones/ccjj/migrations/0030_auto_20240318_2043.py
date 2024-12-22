# Generated by Django 3.2.6 on 2024-03-19 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccjj', '0029_auto_20240315_2011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingresoconciliacion',
            name='toting_con',
        ),
        migrations.AddField(
            model_name='ingresoconciliacion',
            name='estado_con',
            field=models.FloatField(blank=True, null=True, verbose_name='Estado Ingreso Conciliacion'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='dir_per',
            field=models.CharField(max_length=200, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='ema_per',
            field=models.EmailField(blank=True, max_length=300, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='numcel_per',
            field=models.CharField(blank=True, max_length=9, null=True, verbose_name='Número de Celular'),
        ),
    ]