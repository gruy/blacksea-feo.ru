# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-26 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0006_auto_20160908_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ('order',), 'verbose_name': '\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u044f', 'verbose_name_plural': '\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438'},
        ),
        migrations.AddField(
            model_name='room',
            name='is_visible',
            field=models.BooleanField(default=False),
        ),
    ]
