# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-26 00:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0012_csvupload_title'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContactImport',
            new_name='Contact',
        ),
    ]