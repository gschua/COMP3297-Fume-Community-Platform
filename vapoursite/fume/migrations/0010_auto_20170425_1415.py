# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 06:15
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fume', '0009_auto_20170425_0046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membertag',
            name='game',
        ),
        migrations.RemoveField(
            model_name='membertag',
            name='member',
        ),
        migrations.RemoveField(
            model_name='membertag',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='games',
        ),
        migrations.AddField(
            model_name='tag',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fume.Game'),
        ),
        migrations.AddField(
            model_name='tag',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reward',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2017, 8, 23, 6, 15, 10, 264211, tzinfo=utc), verbose_name='Date of Expiry'),
        ),
        migrations.DeleteModel(
            name='MemberTag',
        ),
    ]
