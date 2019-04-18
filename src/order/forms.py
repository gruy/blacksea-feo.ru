# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import  ugettext_lazy as _

from src.rooms.models import Room


def get_rooms():
    rooms = Room.objects.filter(is_visible=True)
    return [(r.id, r.title) for r in rooms]


ROOMS = get_rooms()


def get_room(id):
    for room in ROOMS:
        if int(room[0]) == int(id):
            return room[1]


class OrderForm(forms.Form):
    name = forms.CharField(label=_(u'Имя'))
    phone = forms.CharField(label=_(u'Телефон'))
    email = forms.EmailField(label=_(u'Электронная почта'))
    room = forms.ChoiceField(choices=ROOMS, label=_(u'Тип номера'))
    people = forms.IntegerField(label=_(u'Количество приезжающих'))
    dates = forms.CharField(label=_(u'Предположительные даты проживания'))

    def __init__(self, room_id, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['room'].initial = room_id
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def send(self):
        text = u'Бронирование номера\r\n\r\nКлиент: %s\r\nТелефон: %s\r\nE-mail: %s\r\nНомер: %s\r\nПредполагаемая дата: %s\r\nКоличество приезжающих: %s\r\n' % (
            self.cleaned_data['name'],
            self.cleaned_data['phone'],
            self.cleaned_data['email'],
            get_room(self.cleaned_data['room']),
            self.cleaned_data['dates'],
            self.cleaned_data['people']
        )
        for recipient in settings.EMAIL_RECIPIENTS:
            send_mail(u'Бронирование номера', text, self.cleaned_data['email'], [recipient, ], fail_silently=False)
