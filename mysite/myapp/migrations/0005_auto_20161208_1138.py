# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-08 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20160826_0427'),
    ]

    operations = [
        migrations.AddField(
            model_name='wordsuse',
            name='autotrans',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='wordsuse',
            name='aparitions',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wordsuse',
            name='click',
            field=models.IntegerField(default=0),
        ),
    ]
