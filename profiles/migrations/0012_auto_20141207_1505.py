# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_auto_20141207_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='partner',
        ),
        migrations.AddField(
            model_name='membership',
            name='partner',
            field=models.OneToOneField(blank=True, related_name='partner_of', to='profiles.Invitation', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='avoid_partner',
            field=models.BooleanField(default=False, help_text='If you check this box, you will definitely not be assigned your partner.'),
            preserve_default=True,
        ),
    ]
