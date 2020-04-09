# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-10 02:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0022_auto_20160609_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='ethnicitydata',
            name='valid_since',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='languagedata',
            name='inferred',
            field=models.NullBooleanField(),
        ),
    ]
