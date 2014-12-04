# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20141204_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avoid',
            field=models.ManyToManyField(help_text='You may still be assigned one of these people.', to='profiles.Profile', null=True, related_name='avoided_by', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='avoid_partner',
            field=models.BooleanField(help_text='If you check this box, it is very unlikely that you will be assigned your partner.', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='prefer',
            field=models.ManyToManyField(help_text='You may still not be assigned any of these people.', to='profiles.Profile', null=True, related_name='prefered_by', blank=True),
            preserve_default=True,
        ),
    ]
