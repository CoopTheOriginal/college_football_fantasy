# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_grabber', '0006_auto_20150415_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerdata',
            name='predicted',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='opponent_score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='your_score',
            field=models.IntegerField(null=True),
        ),
    ]
