# Generated by Django 3.2.6 on 2024-03-15 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccjj', '0027_alter_invitacion_esc_invi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agenda',
            name='url_age',
        ),
        migrations.AddField(
            model_name='agenda',
            name='tipinvi_age',
            field=models.CharField(max_length=150, null=True, verbose_name='Tipo Invitacion'),
        ),
    ]
