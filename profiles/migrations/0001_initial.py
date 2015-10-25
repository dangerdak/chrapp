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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('to_name', models.CharField(max_length=50, unique=True)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('admin', models.BooleanField(default=False)),
                ('wishlist', models.TextField(blank=True)),
                ('avoid_partner', models.BooleanField(default=False, help_text='If you check this box, you will definitely not be assigned your partner.')),
                ('avoid', models.ManyToManyField(null=True, related_name='avoided_by', help_text='You may still be assigned one of these people.', to='profiles.Invitation', blank=True)),
                ('giftgroup', models.ForeignKey(to='profiles.GiftGroup')),
                ('partner', models.OneToOneField(null=True, related_name='partner_of', blank=True, to='profiles.Invitation')),
                ('prefer', models.ManyToManyField(null=True, related_name='prefered_by', help_text='You may still not be assigned any of these people.', to='profiles.Invitation', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
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
            field=models.OneToOneField(null=True, related_name='santa_membership', blank=True, to='profiles.Profile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='giftgroup',
            name='members',
            field=models.ManyToManyField(null=True, through='profiles.Membership', to='profiles.Profile', blank=True),
            preserve_default=True,
        ),
    ]
