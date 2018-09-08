# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-30 09:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20180828_2137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Browse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('browse_time', models.DateTimeField(auto_now_add=True)),
                ('goobs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Goods')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.User')),
            ],
            options={
                'db_table': 'browse',
            },
        ),
        migrations.AlterField(
            model_name='pattern',
            name='pattimg',
            field=models.ImageField(null=True, upload_to='pattern'),
        ),
    ]
