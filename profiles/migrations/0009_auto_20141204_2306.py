# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20141204_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avoid_partner',
            field=models.BooleanField(help_text='If you check this box, you will definitely not be assigned your partner.', default=False),
            preserve_default=True,
        ),
    ]
