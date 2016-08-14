# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_grabber', '0007_auto_20150530_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='season',
            field=models.IntegerField(default=2015),
            preserve_default=False,
        ),
    ]
