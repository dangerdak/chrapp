# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_profile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='to_name',
            field=models.CharField(max_length=50),
        ),
    ]
