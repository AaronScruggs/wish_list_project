# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-15 23:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish_list_items', '0008_auto_20160414_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='pledge',
            name='charge_id',
            field=models.CharField(default='none', max_length=128),
            preserve_default=False,
        ),
    ]
