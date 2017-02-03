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
            name='Notificaciones',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('tipo', models.IntegerField()),
                ('tipo_id', models.IntegerField()),
                ('user_for', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('count', models.BigIntegerField()),
                ('view', models.BigIntegerField()),
                ('type_for', models.BigIntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='User')),
            ],
            options={
                'verbose_name_plural': 'Notificacioness',
                'verbose_name': 'Notificaciones',
            },
        ),
    ]
