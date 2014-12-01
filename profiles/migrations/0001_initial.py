# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('wishlist', models.TextField(blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('avoid', models.ManyToManyField(related_name='avoid_rel_+', blank=True, null=True, to='profiles.Profile')),
                ('prefer', models.ManyToManyField(related_name='prefer_rel_+', blank=True, null=True, to='profiles.Profile')),
                ('recipient', models.OneToOneField(to='profiles.Profile', blank=True, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_profile', 'Can view profile'),),
            },
            bases=(models.Model,),
        ),
    ]
