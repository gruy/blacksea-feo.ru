# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-12-10 09:37
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_indexpage_contacts_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexpage',
            name='order_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='', max_length=2000, verbose_name='\u0422\u0435\u043a\u0441\u0442 \u0431\u043b\u043e\u043a\u0430 \u0431\u0440\u043e\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f'),
            preserve_default=False,
        ),
    ]
