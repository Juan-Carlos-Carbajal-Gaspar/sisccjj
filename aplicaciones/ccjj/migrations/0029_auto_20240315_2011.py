# Generated by Django 3.2.6 on 2024-03-16 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccjj', '0028_auto_20240314_2040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='egresodetalle',
            name='totegre_con',
        ),
        migrations.AlterField(
            model_name='egresodetalle',
            name='fecegre_det',
            field=models.DateTimeField(verbose_name='Fecha Egreso'),
        ),
        migrations.AlterField(
            model_name='egresodetalle',
            name='monegre_det',
            field=models.FloatField(blank=True, verbose_name='Monto Egreso'),
        ),
    ]
