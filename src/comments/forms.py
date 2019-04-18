# -*- coding: utf-8 -*-
import urllib
import urllib2
import json

from django import forms
from django.conf import settings
from django.utils.translation import  ugettext_lazy as _

from django_comments.forms import CommentForm


class CommentRecaptchaForm(CommentForm):
    def clean(self):
        recaptcha_response = self.data.get('g-recaptcha-response')
        print recaptcha_response

        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = json.load(response)
        ''' End reCAPTCHA validation '''

        if result['success']:
            return CommentForm.clean(self)
        else:
            raise forms.ValidationError(u'Invalid reCAPTCHA. Please try again.')
