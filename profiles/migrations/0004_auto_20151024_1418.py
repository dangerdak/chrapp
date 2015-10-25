# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_remove_profile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.SlugField(default='dak', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='to_email',
            field=models.EmailField(max_length=254),
        ),
    ]
