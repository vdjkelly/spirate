# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notificaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificaciones',
            name='user',
            field=models.IntegerField(),
        ),
    ]
