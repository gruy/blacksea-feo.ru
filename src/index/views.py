# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from django.views.generic.list import ListView

from src.dashboard.models import IndexPage
from src.photos.models import Photo, Slider
from src.rooms.models import Room
from src.services.models import Service


class MenuMixin(object):
    def menu(self):
        menus = OrderedDict()
        menus['rooms'] = {
            'title': u'Номера и цены',
            'url': reverse('rooms'),
            'is_active': False,
            'submenu': [],
        }

        rooms = Room.objects.filter(is_visible=True)
        for room in rooms:
            menus['rooms']['submenu'].append({
                'title': room.title,
                'url': reverse('room', args=[room.id, ]),
            })

        menus['gallery'] = {
            'title': u'Фотогалерея',
            'url': reverse('gallery'),
            'is_active': False,
            'submenu': [],
        }

        menus['services'] = {
            'title': u'Дополнительные услуги',
            'url': reverse('services'),
            'is_active': False,
            'submenu': [],
        }
        services = Service.objects.all()
        for service in services:
            menus['services']['submenu'].append({
                'title': service.title,
                'url': reverse('service', args=[service.id, ]),
            })

        menus['comments'] = {
            'title': u'Отзывы',
            'url': reverse('comments'),
            'is_active': False,
            'submenu': [],
        }

        menus['contacts'] = {
            'title': u'Контакты',
            'url': reverse('contacts'),
            'is_active': False,
            'submenu': [],
        }

        return menus

    def get_context_data(self, **kwargs):
        context = super(MenuMixin, self).get_context_data(**kwargs)
        context['menu'] = self.menu()
        return context

class IndexView(MenuMixin, TemplateView):
    template_name = 'index/index.html'

    def get(self, request, *args, **kwargs):
        self.sliders = Slider.objects.all()
        self.page, created = IndexPage.objects.get_or_create(pk=1)
        self.rooms = Room.objects.filter(is_visible=True)
        self.services = Service.objects.all()
        super(IndexView, self).get(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['page'] = self.page
        context['sliders'] = self.sliders
        context['rooms'] = self.rooms
        context['services'] = self.services
        return context


class RoomsView(MenuMixin, ListView):
    context_object_name = 'rooms'
    model = Room
    queryset = Room.objects.filter(is_visible=True)
    template_name = 'index/rooms_2.html'

    def get_context_data(self, **kwargs):
        context = super(RoomsView, self).get_context_data(**kwargs)
        context['menu']['rooms']['is_active'] = True
        return context


class RoomDetailView(MenuMixin, DetailView):
    context_object_name = 'room'
    model = Room
    template_name = 'index/room_3.html'

    def get(self, request, *args, **kwargs):
        self.services = Service.objects.all()
        super(RoomDetailView, self).get(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(RoomDetailView, self).get_context_data(**kwargs)
        context['menu']['rooms']['is_active'] = True
        context['services'] = self.services
        return context


class GalleryView(MenuMixin, ListView):
    context_object_name = 'photos'
    model = Photo
    template_name = 'index/gallery.html'

    def get_context_data(self, **kwargs):
        context = super(GalleryView, self).get_context_data(**kwargs)
        context['menu']['gallery']['is_active'] = True
        return context


class ServicesView(MenuMixin, ListView):
    context_object_name = 'services'
    model = Service
    queryset = Service.objects.all()
    template_name = 'index/services.html'

    def get_context_data(self, **kwargs):
        context = super(ServicesView, self).get_context_data(**kwargs)
        context['menu']['services']['is_active'] = True
        return context


class ServiceDetailView(MenuMixin, DetailView):
    context_object_name = 'service'
    model = Service
    template_name = 'index/service.html'

    def get(self, request, *args, **kwargs):
        self.services = Service.objects.exclude(pk=kwargs['pk'])
        super(ServiceDetailView, self).get(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(ServiceDetailView, self).get_context_data(**kwargs)
        context['menu']['services']['is_active'] = True
        context['services'] = self.services
        return context


class ContactsView(MenuMixin, TemplateView):
    template_name = 'index/contacts.html'

    def get(self, request, *args, **kwargs):
        self.page, created = IndexPage.objects.get_or_create(pk=1)
        super(ContactsView, self).get(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data(**kwargs)
        context['menu']['services']['is_active'] = True
        context['contacts'] = self.page
        return context


class CommentsView(MenuMixin, TemplateView):
    template_name = 'index/comments.html'
