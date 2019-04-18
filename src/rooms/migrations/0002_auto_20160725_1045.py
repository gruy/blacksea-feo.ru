# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-25 07:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comfort',
            options={'ordering': ('order',), 'verbose_name': '\u0423\u0434\u043e\u0431\u0441\u0442\u0432\u043e', 'verbose_name_plural': '\u0423\u0434\u043e\u0431\u0441\u0442\u0432\u0430'},
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'verbose_name': '\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u044f', 'verbose_name_plural': '\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438'},
        ),
        migrations.AlterModelOptions(
            name='price',
            options={'verbose_name': '\u0426\u0435\u043d\u0430', 'verbose_name_plural': '\u0426\u0435\u043d\u044b'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ('rooms', 'persons'), 'verbose_name': '\u041d\u043e\u043c\u0435\u0440', 'verbose_name_plural': '\u041d\u043e\u043c\u0435\u0440\u0430'},
        ),
        migrations.AlterField(
            model_name='comfort',
            name='text',
            field=models.TextField(max_length=1024, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='comfort',
            name='title',
            field=models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.CASCADE, to='filer.Image'),
        ),
        migrations.AlterField(
            model_name='price',
            name='date_end',
            field=models.DateField(blank=True, null=True, verbose_name='\u041f\u043e'),
        ),
        migrations.AlterField(
            model_name='price',
            name='date_start',
            field=models.DateField(blank=True, null=True, verbose_name='\u0421'),
        ),
        migrations.AlterField(
            model_name='price',
            name='price_max',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u0414\u043e'),
        ),
        migrations.AlterField(
            model_name='price',
            name='price_min',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u041e\u0442'),
        ),
        migrations.AlterField(
            model_name='price',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='room',
            name='comforts',
            field=models.ManyToManyField(to='rooms.Comfort', verbose_name='\u0423\u0434\u043e\u0431\u0441\u0442\u0432\u0430'),
        ),
        migrations.AlterField(
            model_name='room',
            name='persons',
            field=models.IntegerField(verbose_name='\u041c\u0430\u043a\u0438\u043c\u0430\u043b\u044c\u043d\u043e\u0435 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0447\u0435\u043b\u043e\u0432\u0435\u043a'),
        ),
        migrations.AlterField(
            model_name='room',
            name='places',
            field=models.IntegerField(verbose_name='\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0435 \u043c\u0435\u0441\u0442\u043e'),
        ),
        migrations.AlterField(
            model_name='room',
            name='places_additional',
            field=models.IntegerField(verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u043c\u0435\u0441\u0442\u043e'),
        ),
        migrations.AlterField(
            model_name='room',
            name='quantity',
            field=models.IntegerField(verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043d\u043e\u043c\u0435\u0440\u043e\u0432'),
        ),
        migrations.AlterField(
            model_name='room',
            name='rooms',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043a\u043e\u043c\u043d\u0430\u0442'),
        ),
        migrations.AlterField(
            model_name='room',
            name='title',
            field=models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043d\u043e\u043c\u0435\u0440\u0430'),
        ),
    ]
