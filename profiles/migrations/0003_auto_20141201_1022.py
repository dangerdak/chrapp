# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20141201_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='recipient',
            field=models.OneToOneField(to='profiles.Profile', null=True, related_name='santa', blank=True),
            preserve_default=True,
        ),
    ]
