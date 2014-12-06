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
            name='GiftGroup',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('to_name', models.CharField(max_length=50)),
                ('to_email', models.EmailField(max_length=75)),
                ('key', models.CharField(max_length=20)),
                ('gift_group', models.ForeignKey(to='profiles.GiftGroup')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('wishlist', models.TextField(blank=True)),
                ('avoid_partner', models.BooleanField(default=False, help_text='If you check this box, you will definitely not be assigned your partner.')),
                ('avoid', models.ManyToManyField(null=True, blank=True, related_name='avoided_by', to='profiles.Invitation', help_text='You may still be assigned one of these people.')),
                ('giftgroup', models.ForeignKey(to='profiles.GiftGroup')),
                ('prefer', models.ManyToManyField(null=True, blank=True, related_name='prefered_by', to='profiles.Invitation', help_text='You may still not be assigned any of these people.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('partner', models.OneToOneField(related_name='partner_of', null=True, blank=True, to='profiles.Invitation')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('view_profile', 'Can view profile'), ('send_invites', 'Can send invites'), ('assign_pairs', 'Can assign Santa-recipient pairs')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='membership',
            name='profile',
            field=models.ForeignKey(to='profiles.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='membership',
            name='recipient',
            field=models.OneToOneField(related_name='santa', null=True, blank=True, to='profiles.Invitation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='giftgroup',
            name='admin',
            field=models.ManyToManyField(to='profiles.Profile', related_name='admin_of'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='giftgroup',
            name='members',
            field=models.ManyToManyField(null=True, blank=True, through='profiles.Membership', to='profiles.Profile'),
            preserve_default=True,
        ),
    ]
