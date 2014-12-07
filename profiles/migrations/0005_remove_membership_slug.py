# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20141206_2028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='slug',
        ),
    ]
