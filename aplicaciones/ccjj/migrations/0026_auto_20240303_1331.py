# Generated by Django 3.2.6 on 2024-03-03 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ccjj', '0025_auto_20240303_1221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingresocopias',
            old_name='id_cli_cop',
            new_name='id_cli',
        ),
        migrations.AlterField(
            model_name='ingresoconciliaciondetalle',
            name='id_cli',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ccjj.cliente', verbose_name='id Cliente'),
        ),
    ]
