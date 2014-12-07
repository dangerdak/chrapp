# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_remove_membership_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='recipient',
            field=models.OneToOneField(null=True, to='profiles.Profile', related_name='member_of', blank=True),
            preserve_default=True,
        ),
    ]
