# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-20 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0010_contactimport'),
    ]

    operations = [
        migrations.CreateModel(
            name='CsvUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='imports/')),
            ],
        ),
    ]
