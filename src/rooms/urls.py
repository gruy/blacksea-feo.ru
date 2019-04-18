# -*- coding: utf-8 -*-
from django.conf.urls import url

from src.rooms.views import *


urlpatterns = [
    url(r'^rooms/$', RoomListView.as_view(), name='rooms'),
    url(r'^rooms/(?P<pk>\d+)/$', RoomDetailView.as_view(), name='room'),
    url(r'^appartments/$', AppartmentListView.as_view(), name='appartments'),
    url(r'^appartments/(?P<pk>\d+)/$', AppartmentDetailView.as_view(), name='appartment'),
]
