# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20141207_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='recipient',
            field=models.ForeignKey(to='profiles.Profile', related_name='santa_memberships', blank=True, null=True),
            preserve_default=True,
        ),
    ]
