# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish_list_items', '0010_auto_20160418_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishitem',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='wishitem',
            name='item_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]