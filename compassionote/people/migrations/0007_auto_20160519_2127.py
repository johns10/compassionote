# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-20 01:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_auto_20160519_2119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dobrange',
            name='dob',
        ),
        migrations.AddField(
            model_name='dob',
            name='end',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='dob',
            name='start',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='apartment',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='building',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='house_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street_prefix',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='dob',
            name='valid_since',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='email_address_md5',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='email_provider',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='email',
            name='valid_since',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='display',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='region',
            field=models.CharField(choices=[('us', 'United States')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='name',
            name='first',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='name',
            name='last',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='name',
            name='middle',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='name',
            name='suffix',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='match',
            field=models.DecimalField(decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='search_pointer',
            field=models.CharField(max_length=8192, null=True),
        ),
        migrations.AlterField(
            model_name='phone',
            name='country_code',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='phone',
            name='display',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='phone',
            name='display_international',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='phone',
            name='type',
            field=models.CharField(choices=[('work_phone', 'Work Phone'), ('home_phone', 'Home Phone'), ('work_fax', 'Work Fax'), ('mobile', 'Mobile Phone'), ('home_fax', 'Home Fax'), ('pager', 'Pager')], max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='phone',
            name='valid_since',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='first',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='last',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='middle',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='valid_since',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='category',
            field=models.CharField(choices=[('background_reports', 'Background Reports'), ('contact_details', 'Contact Details'), ('email_addresses', 'Email Addresses'), ('media', 'Media'), ('personal_profiles', 'Personal Profiles'), ('professional_and_business', 'Professional and Business'), ('public_records', 'Public Records'), ('publications', 'Publications'), ('school_and_classmates', 'School and Classmates'), ('web_pages', 'Web Pages')], max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='domain',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='url',
            name='name',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='userid',
            name='valid_since',
            field=models.DateField(null=True),
        ),
        migrations.DeleteModel(
            name='DobRange',
        ),
    ]
