# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_grabber', '0008_game_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='playerdata',
            name='extra_point_kick',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerdata',
            name='three_point_kick',
            field=models.IntegerField(default=0),
        ),
    ]
