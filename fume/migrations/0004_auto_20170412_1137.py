# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 03:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fume', '0003_auto_20170410_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date/time of registration'),
        ),
    ]