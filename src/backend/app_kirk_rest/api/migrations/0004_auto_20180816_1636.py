# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-16 23:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180816_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replicationjobs',
            name='jobLabel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]