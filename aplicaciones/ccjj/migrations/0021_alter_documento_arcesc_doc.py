# Generated by Django 3.2.6 on 2024-03-02 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccjj', '0020_auto_20231028_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='arcesc_doc',
            field=models.FileField(blank=True, null=True, upload_to='Documentos/%Y/%m/%d', verbose_name='Documentos'),
        ),
    ]