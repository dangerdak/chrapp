# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20141201_1022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': (('view_profile', 'Can view profile'), ('send_invites', 'Can send invites'), ('assign_pairs', 'Can assign Santa-recipient pairs'))},
        ),
    ]
