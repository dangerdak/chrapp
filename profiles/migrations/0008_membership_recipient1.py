# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20141207_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='recipient1',
            field=models.ForeignKey(to='profiles.Profile', null=True, blank=True, related_name='santa_membership1'),
            preserve_default=True,
        ),
    ]
