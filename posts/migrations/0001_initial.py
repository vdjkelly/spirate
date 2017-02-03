# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import posts.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='categorias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=180, unique=True)),
                ('slug', models.SlugField(max_length=180, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='imagen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('file', models.ImageField(upload_to=posts.models.imagen.file_upload)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='posts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('titulo', models.CharField(max_length=240, unique=True)),
                ('slug', models.SlugField(max_length=240, editable=False)),
                ('cuerpo', models.TextField()),
                ('tags', models.CharField(max_length=180)),
                ('img_file', models.CharField(max_length=240)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('permitir_comentarios', models.BooleanField(default=True)),
                ('shared', models.PositiveIntegerField(default=0)),
                ('favs', models.PositiveIntegerField(default=0)),
                ('comentarios', models.PositiveIntegerField(default=0)),
                ('follows', models.PositiveIntegerField(default=0)),
                ('puntos', models.PositiveIntegerField(default=0)),
                ('sticky', models.PositiveIntegerField(default=0)),
                ('follow', models.PositiveIntegerField(default=0)),
                ('ip_autor', models.IPAddressField(default=0)),
                ('autoria_link', models.URLField()),
                ('categoria', models.ForeignKey(related_name='posts', to='posts.categorias')),
                ('user', models.ForeignKey(related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Puntos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('puntos', models.PositiveIntegerField(default=0)),
                ('time_p', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(related_name='Puntos', to='posts.posts')),
                ('user', models.ForeignKey(related_name='Puntos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
