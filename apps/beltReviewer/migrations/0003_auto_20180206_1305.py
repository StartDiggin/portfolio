# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-06 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beltReviewer', '0002_auto_20180206_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
