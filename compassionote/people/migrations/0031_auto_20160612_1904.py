# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-12 23:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0030_auto_20160612_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdata',
            name='apartment',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='contactdata',
            name='building',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]