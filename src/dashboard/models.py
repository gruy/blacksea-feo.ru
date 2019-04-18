# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from ckeditor_uploader.fields import RichTextUploadingField


@python_2_unicode_compatible  # only if you need to support Python 2
class IndexPage(models.Model):
    text = RichTextUploadingField(u'Текст главной страницы', max_length=20000)
    contacts_text = RichTextUploadingField(u'Дополнительная информация о контактах, бронировании, трансфере', max_length=20000)
    phone_1 = models.CharField(u'Телефон 1', max_length=255, blank=True, null=True)
    phone_2 = models.CharField(u'Телефон 2', max_length=255, blank=True, null=True)
    phone_3 = models.CharField(u'Телефон 3', max_length=255, blank=True, null=True)
    address = models.CharField(u'Адрес', max_length=255, blank=True, null=True)
    email = models.CharField(u'Электронная почта', max_length=255, blank=True, null=True)
    skype = models.CharField(u'Скайп', max_length=255, blank=True, null=True)
    map = models.TextField(u'Код для карты', max_length=2000, blank=True, null=True)

    class Meta(object):
        verbose_name = u'Главная страница'
        verbose_name_plural = u'Главные страницы'

    def __str__(self):
        return u'%s' % (self.pk,)
