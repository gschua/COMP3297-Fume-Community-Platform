# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 14:06
from __future__ import unicode_literals

from django.db import migrations, models
import fume.models


class Migration(migrations.Migration):

    dependencies = [
        ('fume', '0002_auto_20170410_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=fume.models.upload_path_handler),
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='password',
            field=models.CharField(max_length=254),
        ),
    ]
