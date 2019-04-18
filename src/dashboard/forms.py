# -*- coding: utf-8 -*-
from django.forms import Form, ModelForm


from src.dashboard.models import IndexPage


class IndexPageForm(ModelForm):
    class Meta:
        fields = ['text', ]
        model = IndexPage


class ContactsForm(ModelForm):
    class Meta:
        fields = ['contacts_text', 'phone_1', 'phone_2', 'phone_3', 'address', 'email', 'skype', 'map', ]
        model = IndexPage
