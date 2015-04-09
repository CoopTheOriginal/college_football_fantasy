# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('team', models.CharField(max_length=100)),
                ('game_date', models.DateField()),
                ('opponent', models.CharField(max_length=100)),
                ('your_score', models.IntegerField()),
                ('opponent_score', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Passing',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('attempts', models.IntegerField()),
                ('completions', models.IntegerField()),
                ('yards', models.IntegerField()),
                ('touchdowns', models.IntegerField()),
                ('interceptions', models.IntegerField()),
                ('game', models.ForeignKey(to='data_grabber.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('team', models.CharField(max_length=100)),
                ('position', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('ext_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Rushing',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('attempts', models.IntegerField()),
                ('yards', models.IntegerField()),
                ('touchdowns', models.IntegerField()),
                ('game', models.ForeignKey(to='data_grabber.Game')),
                ('player', models.ForeignKey(to='data_grabber.Player')),
            ],
        ),
        migrations.AddField(
            model_name='passing',
            name='player',
            field=models.ForeignKey(to='data_grabber.Player'),
        ),
    ]
