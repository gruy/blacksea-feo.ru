# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import os

from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
from filer.fields.image import FilerImageField


def upl(instance, filename):
    f = '{0}{1}'.format(hashlib.md5(filename.encode('utf8')).hexdigest(), os.path.splitext(filename)[1])
    return 'services/{0}'.format(f)


class Service(models.Model):
    title = models.CharField(u'Название', max_length=255)
    image = models.ImageField(u'Фотография', upload_to=upl)
    mini_text = models.CharField(u'Краткое описание', max_length=255)
    text = RichTextUploadingField(u'Описание', max_length=20000)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta(object):
        ordering = ('order',)

    def __str__(self):
        return u'%s' % (self.id)

    def get_photos(self):
        return self.photos.all()


class ServicePhoto(models.Model):
    service = models.ForeignKey(Service, related_name='photos')
    image = models.ImageField(upload_to=upl)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ('order',)
        verbose_name = u'Фотография'
        verbose_name_plural = u'Фотографии'

#    def __str__(self):
#        return u'%s' % (self.service.title)
