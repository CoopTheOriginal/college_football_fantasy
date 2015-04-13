# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_grabber', '0003_auto_20150410_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerData',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('pass_attempts', models.IntegerField(null=True)),
                ('pass_completions', models.IntegerField(null=True)),
                ('pass_yards', models.IntegerField(null=True)),
                ('pass_touchdowns', models.IntegerField(null=True)),
                ('interceptions', models.IntegerField(null=True)),
                ('rush_attempts', models.IntegerField(null=True)),
                ('rush_yards', models.IntegerField(null=True)),
                ('rush_touchdowns', models.IntegerField(null=True)),
                ('rec_yards', models.IntegerField(null=True)),
                ('rec_touchdowns', models.IntegerField(null=True)),
                ('receptions', models.IntegerField(null=True)),
                ('game', models.ForeignKey(to='data_grabber.Game')),
                ('player', models.ForeignKey(to='data_grabber.Player')),
            ],
        ),
        migrations.RemoveField(
            model_name='stats',
            name='game',
        ),
        migrations.RemoveField(
            model_name='stats',
            name='player',
        ),
        migrations.DeleteModel(
            name='Stats',
        ),
    ]
