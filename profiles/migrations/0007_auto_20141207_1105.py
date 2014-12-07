# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20141207_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='recipient',
            field=models.OneToOneField(null=True, blank=True, related_name='santa_membership', to='profiles.Profile'),
            preserve_default=True,
        ),
    ]
