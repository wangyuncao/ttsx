# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-30 09:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20180830_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='browse',
            name='goods',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='web.Goods'),
        ),
    ]