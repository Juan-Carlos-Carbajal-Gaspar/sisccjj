# Generated by Django 3.2.6 on 2023-10-04 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccjj', '0011_acta_agenda_cajaconciliacion_categoria_conciliador_constanciainvitado_constanciasolicitante_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingresoconciliacion',
            name='desc_con',
            field=models.FloatField(blank=True, null=True, verbose_name='Descuento Conciliacion'),
        ),
    ]
