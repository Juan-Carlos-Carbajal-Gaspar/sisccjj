# Generated by Django 3.2.6 on 2024-03-20 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccjj', '0031_alter_ingresoconciliacion_estado_con'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='egresodetalle',
            name='fecegre_det',
        ),
        migrations.AddField(
            model_name='egresodetalle',
            name='fecegredet_con',
            field=models.DateField(null=True, verbose_name='Fecha Egreso Conciliacion Detalle'),
        ),
        migrations.AddField(
            model_name='egresodetalle',
            name='horegredet_con',
            field=models.TimeField(null=True, verbose_name='Hora Egreso Conciliacion Detalle'),
        ),
    ]