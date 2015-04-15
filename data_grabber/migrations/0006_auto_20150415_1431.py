# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_grabber', '0005_auto_20150414_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerdata',
            name='interceptions',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerdata',
            name='pass_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerdata',
            name='pass_completions',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerdata',
            name='pass_touchdowns',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerdata',
            name='pass_yards',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerdata',
            name='rec_touchdowns',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerdata',
            name='rec_yards',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerdata',
            name='receptions',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerdata',
            name='rush_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerdata',
            name='rush_touchdowns',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='playerdata',
            name='rush_yards',
            field=models.IntegerField(default=0),
        ),
    ]
