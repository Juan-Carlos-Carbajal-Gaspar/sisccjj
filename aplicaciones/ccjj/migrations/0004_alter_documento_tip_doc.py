# Generated by Django 3.2.6 on 2023-08-27 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccjj', '0003_auto_20230821_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='tip_doc',
            field=models.CharField(max_length=100, verbose_name='Tipo de Documento'),
        ),
    ]
