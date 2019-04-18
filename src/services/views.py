# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from src.photos.models import Photo, TAGS_CHOICES


class PhotosView(TemplateView):

    template_name = 'photos.html'

    def get_context_data(self, **kwargs):
        context = super(PhotosView, self).get_context_data(**kwargs)
        context['photos'] = Photo.objects.all()
        tags = list(set(Photo.objects.values_list('tag', flat=True)))
        context['tags'] = [tag for tag in TAGS_CHOICES if tag[0] in tags]
        return context
