# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=65)),
                ('department', models.ForeignKey(blank=True, to='auth.Group', null=True)),
            ],
            options={
                'permissions': ((b'read_position', b'Can read position'),),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='position',
            unique_together=set([(b'name', b'department')]),
        ),
    ]
