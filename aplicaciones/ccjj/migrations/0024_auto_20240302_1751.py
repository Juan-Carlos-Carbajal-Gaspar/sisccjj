# Generated by Django 3.2.6 on 2024-03-02 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccjj', '0023_alter_documento_arcesc_doc'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='t_doc',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Tipo de Documentos'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='tip_doc',
            field=models.CharField(max_length=100, verbose_name='Titulo de Documento'),
        ),
    ]
