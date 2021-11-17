# Generated by Django 3.1.2 on 2021-11-03 18:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ElegirRespuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correcta', models.BooleanField(default=False, verbose_name='Es esta la respuesta correcta?')),
                ('texto', models.TextField(verbose_name='Texto de la respuesta')),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(verbose_name='Texto de la Pregunta')),
                ('max_puntaje', models.DecimalField(decimal_places=2, default=3, max_digits=6, verbose_name='Maximo Puntaje')),
                ('archivo', models.FileField(blank=True, null=True, upload_to='imagenes_quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Proceso',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombreproceso', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=100)),
                ('tipo_quiz', models.CharField(choices=[('1', 'Preguntas'), ('2', 'Dados'), ('3', 'Cartas')], default='3', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='QuizUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntaje_total', models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='puntaje total')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PreguntasRespondidas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correcta', models.BooleanField(default=False, verbose_name='Es esta la pregunta correcta?s')),
                ('puntaje_obtenido', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Puntaje Obtenido')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.pregunta')),
                ('quizUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intentos', to='app.quizusuario')),
                ('respuesta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.elegirrespuesta')),
            ],
        ),
        migrations.AddField(
            model_name='pregunta',
            name='proceso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.proceso'),
        ),
        migrations.AddField(
            model_name='elegirrespuesta',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opciones', to='app.pregunta'),
        ),
        migrations.CreateModel(
            name='CampanaAsignada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finalizo_campana', models.IntegerField(default=0)),
                ('procesoasignado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.proceso')),
                ('usuarioasignado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]