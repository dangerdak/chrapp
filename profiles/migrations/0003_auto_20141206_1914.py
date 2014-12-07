# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_membership_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='recipient',
            field=models.OneToOneField(related_name='santa', to='profiles.Profile', null=True, blank=True),
            preserve_default=True,
        ),
    ]
