from django.conf.urls import url
from django.views.generic import TemplateView

from src.index.views import *


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^contacts/$', ContactsView.as_view(), name='contacts'),
    url(r'^otzyvy/$', CommentsView.as_view(), name='comments'),
    url(r'^gallery/$', GalleryView.as_view(), name='gallery'),
    url(r'^rooms/$', RoomsView.as_view(), name='rooms'),
    url(r'^rooms/(?P<pk>\d+)/$', RoomDetailView.as_view(), name='room'),
    url(r'^services/$', ServicesView.as_view(), name='services'),
    url(r'^services/(?P<pk>\d+)/$', ServiceDetailView.as_view(), name='service'),
    url(r'^search/$', SearchView.as_view(), name='search'),
]
