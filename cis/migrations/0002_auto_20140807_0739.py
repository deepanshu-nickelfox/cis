# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('cis', '0001_initial'),
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, blank=True, to='hr.Position', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', verbose_name='user permissions', blank=True),
            preserve_default=True,
        ),
    ]
