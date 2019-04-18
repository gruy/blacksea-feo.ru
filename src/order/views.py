# -*- coding: utf-8 -*-
import json

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.template.loader import render_to_string

from src.order.forms import OrderForm


def order(request):
    resp = {'result': 'error', }

    room_id = request.GET.get('room')

    if request.method == 'POST':
        form = OrderForm(data=request.POST, room_id=room_id)
        if form.is_valid():
            form.send()
#             request.order_form_message = u'Ваш заказ на бронирование отправлен'
            resp['result'] = 'success'
            form = OrderForm(room_id=room_id)
    else:
        form = OrderForm(room_id=room_id)

    resp['html'] = render_to_string('order/form.html', {
        'form': form,
        }, context_instance=RequestContext(request)
    )
    response = json.dumps(resp)
    return HttpResponse(response, content_type='application/json')
