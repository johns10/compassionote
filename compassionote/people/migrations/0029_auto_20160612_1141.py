# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-12 15:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0028_auto_20160611_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressdata',
            name='valid_since',
            field=models.DateField(blank=True, null=True),
        ),
    ]