# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('pais', models.CharField(max_length=2)),
                ('sexo', models.CharField(max_length=2)),
                ('posts', models.PositiveIntegerField(default=0)),
                ('comentarios', models.PositiveIntegerField(default=0)),
                ('puntos', models.PositiveIntegerField(default=0)),
                ('puntos_dar', models.PositiveIntegerField(default=10)),
                ('seguidores', models.PositiveIntegerField(default=0)),
                ('siguiendo', models.PositiveIntegerField(default=0)),
                ('foto', models.CharField(max_length=240)),
                ('update_puntos', models.PositiveIntegerField(default=0)),
                ('fb_user', models.URLField(unique=True)),
                ('tw_user', models.CharField(max_length=180)),
                ('privacidad', models.CharField(max_length=100)),
                ('fecha_nacimiento', models.DateField(blank=True)),
                ('notificaciones', models.CharField(max_length=2000)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Seguidores',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('tipo', models.IntegerField()),
                ('seguido', models.IntegerField()),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('seguidor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
