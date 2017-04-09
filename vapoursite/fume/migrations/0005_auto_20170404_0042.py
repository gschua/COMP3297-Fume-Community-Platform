# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fume', '0004_auto_20170404_0015'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='platform',
        ),
        migrations.AddField(
            model_name='game',
            name='platform',
            field=models.ManyToManyField(to='fume.Platform'),
        ),
    ]