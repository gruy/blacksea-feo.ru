# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import os

from django.db import models
from django.utils.html import format_html


TAGS_CHOICES = (
    (0, u''),
    (1, u'Дом'),
    (2, u'Двор'),
    (3, u'Комнаты'),
    (4, u'Кухня'),
)


def upl(instance, filename):
    f = '{0}{1}'.format(hashlib.md5(filename.encode('utf8')).hexdigest(), os.path.splitext(filename)[1])
    return 'photos/{0}'.format(f)


class Photo(models.Model):
    image = models.ImageField(upload_to=upl)
    tag = models.IntegerField(choices=TAGS_CHOICES)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta(object):
        ordering = ('order',)


def upl_slider(instance, filename):
    f = '{0}{1}'.format(hashlib.md5(filename.encode('utf8')).hexdigest(), os.path.splitext(filename)[1])
    return 'sliders/{0}'.format(f)


class Slider(models.Model):
    image = models.ImageField(upload_to=upl_slider)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta(object):
        ordering = ('order',)
