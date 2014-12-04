# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_profile_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avoid_partner',
            field=models.BooleanField(help_text='It will be very unlikely that you will be assigned your partner', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='avoid',
            field=models.ManyToManyField(related_name='avoided_by', help_text='You may still be assigned one of these people', to='profiles.Profile', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='prefer',
            field=models.ManyToManyField(related_name='prefered_by', help_text='You may still not be assigned any of these people', to='profiles.Profile', blank=True, null=True),
            preserve_default=True,
        ),
    ]
