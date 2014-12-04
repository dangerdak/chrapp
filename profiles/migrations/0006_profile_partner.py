# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_profile_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='partner',
            field=models.OneToOneField(null=True, blank=True, related_name='partner_of', to='profiles.Profile'),
            preserve_default=True,
        ),
    ]
