# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_grabber', '0002_game_home'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
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
            model_name='passing',
            name='game',
        ),
        migrations.RemoveField(
            model_name='passing',
            name='player',
        ),
        migrations.RemoveField(
            model_name='rushing',
            name='game',
        ),
        migrations.RemoveField(
            model_name='rushing',
            name='player',
        ),
        migrations.DeleteModel(
            name='Passing',
        ),
        migrations.DeleteModel(
            name='Rushing',
        ),
    ]
