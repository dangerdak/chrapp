# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20141203_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='admin',
            field=models.BooleanField(default=False, editable=False),
            preserve_default=True,
        ),
    ]
