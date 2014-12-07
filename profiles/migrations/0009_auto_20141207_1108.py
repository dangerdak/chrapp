# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_membership_recipient1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='recipient1',
        ),
        migrations.AlterField(
            model_name='membership',
            name='recipient',
            field=models.ForeignKey(to='profiles.Profile', blank=True, null=True, related_name='santa_membership'),
            preserve_default=True,
        ),
    ]
