# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 00:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0020_auto_20160606_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='namedata',
            name='valid_since',
            field=models.DateField(blank=True, null=True),
        ),
    ]