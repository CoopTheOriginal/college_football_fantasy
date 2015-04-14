# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_grabber', '0004_auto_20150410_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='week',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playerdata',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
