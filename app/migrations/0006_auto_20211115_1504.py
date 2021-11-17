# Generated by Django 3.1.2 on 2021-11-15 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_tipo_usuario_cargo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipo_usuario',
            name='tipo',
        ),
        migrations.AddField(
            model_name='tipo_usuario',
            name='empresa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa'),
        ),
        migrations.AddField(
            model_name='tipo_usuario',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='media'),
        ),
        migrations.AddField(
            model_name='tipo_usuario',
            name='tipo_de_usuario',
            field=models.CharField(choices=[('1', 'Admin'), ('2', 'Evaluado'), ('3', 'Evaluador')], default='1', max_length=2),
        ),
    ]
