# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='slug',
            field=models.SlugField(unique=True, default='another'),
            preserve_default=False,
        ),
    ]
