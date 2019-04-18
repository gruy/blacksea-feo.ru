# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html

from adminsortable.admin import SortableAdmin
from easy_thumbnails.files import get_thumbnailer

from src.rooms.models import *


class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ('image',)
    readonly_fields = ('image_admin',)


class PriceInline(admin.TabularInline):
    model = Price
    extra = 1


class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ('comforts',)
    inlines = [
        PhotoInline,
        PriceInline,
    ]
    save_on_top = True


admin.site.register(Room, RoomAdmin)
admin.site.register(Comfort, SortableAdmin)
admin.site.register(Photo)
admin.site.register(Price)
