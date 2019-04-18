# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _

from order.forms import OrderForm


class Order(object):
    def process_request(self, request):
        print request.POST.get('order-form')
        if request.method == 'POST' and 'order-form' in request.POST:
            form = OrderForm(request.POST)
            if form.is_valid():
                form.send()
                request.order_form_message = _(u'Ваш заказ на бронирование отправлен')
                form = OrderForm()
        else:
            form = OrderForm()

        request.order_form = form
