# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-11 21:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0025_auto_20160611_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persondata',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='people', to='people.ContactData'),
        ),
    ]
