# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20141207_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='avoid_partner',
            field=models.OneToOneField(null=True, to='profiles.Invitation', blank=True, help_text='If you check this box, you will definitely not be assigned your partner.'),
            preserve_default=True,
        ),
    ]
