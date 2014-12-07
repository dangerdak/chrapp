# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20141206_1914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='giftgroup',
            name='admin',
        ),
        migrations.AddField(
            model_name='membership',
            name='admin',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
