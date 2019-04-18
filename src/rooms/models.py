# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
import os

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import format_html
from django.utils.translation import ugettext as _

from adminsortable.models import SortableMixin
from ckeditor.fields import RichTextField
from easy_thumbnails.files import get_thumbnailer
#from filer.fields.image import FilerImageField


@python_2_unicode_compatible  # only if you need to support Python 2
class Comfort(SortableMixin):
    title = models.CharField(u'Название', max_length=255)
    text = models.TextField(u'Описание', max_length=1024)
    fa_icon = models.CharField(u'Картинка', max_length=255)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta(object):
        ordering = ('order',)
        verbose_name = u'Удобство'
        verbose_name_plural = u'Удобства'

    def __str__(self):
        return self.title


def upl(instance, filename):
    f = '{0}{1}'.format(hashlib.md5(filename.encode('utf8')).hexdigest(), os.path.splitext(filename)[1])
    return 'rooms/{0}'.format(f)


@python_2_unicode_compatible
class Room(models.Model):
    title = models.CharField(u'Название номера', max_length=255)
    quantity = models.IntegerField(u'Количество номеров')
    numbers = models.CharField(u'Какие номера', max_length=255)
    rooms = models.IntegerField(u'Количество комнат', blank=True, null=True)
    persons = models.IntegerField(u'Макс. количество человек')
    places = models.IntegerField(u'Основное место')
    places_additional = models.IntegerField(u'Дополнительное место')
    comforts = models.ManyToManyField(Comfort, verbose_name=u'Удобства')
    text = models.TextField(max_length=500, verbose_name=u'Дополнительное описание номера (не более 500 знаков)', blank=True, null=True)
    is_visible = models.BooleanField(u'Показывать на сайте', default=False)

    class Meta:
        ordering = ('rooms', 'persons',)
        verbose_name = u'Номер'
        verbose_name_plural = u'Номера'

    def __str__(self):
        return self.title

    def get_cover(self):
        try:
            cover = self.photos.filter(cover=True)[:1].get()
        except Photo.DoesNotExist:
            cover = self.photos.all()[:1].get()
        return cover

    def get_photos(self):
        return self.photos.all()

    def get_comforts(self):
        return self.comforts.all()

    def get_prices(self):
        return self.prices.order_by('date_start')

    def get_price_min(self):
        try:
            price = self.prices.order_by('price_min')[:1].get()
        except Price.DoesNotExist:
            price = None
        return price

    def image_admin(self):
        cover = self.get_cover()
        img = get_thumbnailer(cover.image)['room_admin'].url
        return format_html('<img src="{}" />', img)


def upl_photos(instance, filename):
    f = '{0}{1}'.format(hashlib.md5(filename.encode('utf8')).hexdigest(), os.path.splitext(filename)[1])
    return 'rooms/{0}/{1}'.format(instance.room_id, f)


@python_2_unicode_compatible
class Photo(models.Model):
    room = models.ForeignKey(Room, related_name='photos')
#    image = FilerImageField()
    image = models.ImageField(upload_to=upl_photos)
    cover = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ('order',)
        verbose_name = u'Фотография'
        verbose_name_plural = u'Фотографии'

    def __str__(self):
        return self.room.title

    def image_admin(self):
        img = get_thumbnailer(self.image)['room_admin'].url
        return format_html('<img src="{}" />', img)


@python_2_unicode_compatible
class Price(models.Model):
    room = models.ForeignKey(Room, related_name='prices')
    title = models.CharField(u'Название', max_length=255, blank=True, null=True)
    date_start = models.DateField(u'Дата с')
    date_end = models.DateField(u'Дата по')
    price_min = models.IntegerField(u'Цена от', blank=True, null=True)
    price_max = models.IntegerField(u'Цена до', blank=True, null=True)

    class Meta:
        verbose_name = u'Цена'
        verbose_name_plural = u'Цены'

    def __str__(self):
        return u'%s - %s' % (self.date_start.strftime('%d %B %Y'), self.date_end.strftime('%d %B %Y'))
