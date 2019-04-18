from django.conf.urls import url
from django.views.generic import TemplateView

from src.dashboard.views import *


urlpatterns = [
#    url(r'^$', TemplateView.as_view(template_name='dashboard/base.html')),
    url(r'^$', IndexPageView.as_view(), name='index-page'),

    url(r'^contacts/$', ContactsView.as_view(), name='contacts'),

    url(r'^index/$', IndexPageView.as_view(), name='index-page'),
    url(r'^index/slider/(?P<pk>\d+)/delete/$', SliderDeleteView.as_view(), name='slider-delete'),
    url(r'^index/slider/sort/$', SliderSortView.as_view(), name='sliders-sort'),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^rooms/$', RoomsListView.as_view(), name='rooms'),
    url(r'^rooms/add/$', RoomAddView.as_view(), name='room-add'),
    url(r'^rooms/(?P<pk>\d+)/edit/$', RoomEditView.as_view(), name='room-edit'),
    url(r'^rooms/(?P<pk>\d+)/photo/$', RoomPhotoView.as_view(), name='room-photo'),
    url(r'^rooms/(?P<pk>\d+)/photo-sort/$', RoomPhotoSortView.as_view(), name='room-photos-sort'),
    url(r'^rooms/(?P<pk>\d+)/price/$', RoomPriceView.as_view(), name='room-price'),
    url(r'^rooms/(?P<pk>\d+)/photo/(?P<photo_id>\d+)/$', RoomPhotoEditView.as_view(), name='room-photo-edit'),
    url(r'^rooms/(?P<pk>\d+)/price/add/$', RoomPriceAddView.as_view(), name='room-price-add'),
    url(r'^rooms/price/(?P<pk>\d+)/edit/$', RoomPriceEditView.as_view(), name='room-price-edit'),
    url(r'^rooms/price/(?P<pk>\d+)/delete/$', RoomPriceDeleteView.as_view(), name='room-price-delete'),

    url(r'^services/$', ServicesView.as_view(), name='services'),
    url(r'^services/add/$', ServiceAddView.as_view(), name='service-add'),
    url(r'^services/(?P<pk>\d+)/$', ServiceEditView.as_view(), name='service-edit'),
    url(r'^services/(?P<pk>\d+)/photo/$', ServicePhotoView.as_view(), name='service-photo'),
    url(r'^services/(?P<pk>\d+)/photo-sort/$', ServicePhotoSortView.as_view(), name='service-photos-sort'),
    url(r'^service/(?P<pk>\d+)/photo/(?P<photo_id>\d+)/$', ServicePhotoEditView.as_view(), name='service-photo-edit'),

    url(r'^photos/$', PhotoView.as_view(), name='photos'),
    url(r'^photos/(?P<pk>\d+)/delete/$', PhotoDeleteView.as_view(), name='photo-delete'),
    url(r'^photos/sort/$', PhotoSortView.as_view(), name='photos-sort'),
]
