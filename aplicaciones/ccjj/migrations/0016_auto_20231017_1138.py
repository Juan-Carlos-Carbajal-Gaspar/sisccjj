# Generated by Django 3.2.6 on 2023-10-17 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccjj', '0015_auto_20231017_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='informe',
            name='hor_inf',
            field=models.TimeField(null=True, verbose_name='Hora Informe'),
        ),
        migrations.AlterField(
            model_name='informe',
            name='fec_inf',
            field=models.DateField(null=True, verbose_name='Fecha Informe'),
        ),
    ]