# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-12 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fume', '0005_auto_20170412_1927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='platform',
            new_name='platforms',
        ),
        migrations.AlterField(
            model_name='reward',
            name='status',
            field=models.CharField(choices=[('act', 'Active'), ('exp', 'Expired'), ('use', 'Used'), ('car', 'Cart')], default='act', max_length=3),
        ),
    ]