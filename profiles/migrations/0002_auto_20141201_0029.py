# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avoid',
            field=models.ManyToManyField(blank=True, null=True, related_name='avoided_by', to='profiles.Profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='prefer',
            field=models.ManyToManyField(blank=True, null=True, related_name='prefered_by', to='profiles.Profile'),
            preserve_default=True,
        ),
    ]
