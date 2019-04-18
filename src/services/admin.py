# -*- coding: utf-8 -*-
from django.contrib import admin

from src.services.models import Service, ServicePhoto

admin.site.register(Service)
admin.site.register(ServicePhoto)