# Generated by Django 3.1.2 on 2021-11-08 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proceso',
            old_name='nombreproceso',
            new_name='nombre_proceso',
        ),
    ]
