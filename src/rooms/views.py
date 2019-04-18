# -*- coding: utf-8 -*-
from django.db.models import Min
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from src.rooms.models import Room


class RoomListView(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'rooms.html'
    queryset = Room.objects.filter(type=1).annotate(m=Min('prices__price_min')).order_by('m')
    paginate_by = 100


class RoomDetailView(DetailView):

    model = Room
    context_object_name = 'room'
    template_name = 'room.html'

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)
        context['rooms'] = Room.objects.filter(type=1).exclude(pk=context['object'].id)
        return context


class AppartmentListView(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'appartments.html'
    queryset = Room.objects.filter(type=2).annotate(m=Min('prices__price_min')).order_by('m')


class AppartmentDetailView(DetailView):

    model = Room
    context_object_name = 'room'
    template_name = 'appartment.html'

    def get_context_data(self, **kwargs):
        context = super(AppartmentDetailView, self).get_context_data(**kwargs)
        context['rooms'] = Room.objects.filter(type=2).exclude(pk=context['object'].id)
        return context
