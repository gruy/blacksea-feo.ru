# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-02-20 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0008_auto_20170220_1000'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='numbers',
            field=models.CharField(default='', max_length=255, verbose_name='\u041a\u0430\u043a\u0438\u0435 \u043d\u043e\u043c\u0435\u0440\u0430'),
            preserve_default=False,
        ),
    ]
