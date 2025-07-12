from django.contrib import admin
from .models import Place, Image
from django.utils.html import format_html

class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'lat', 'lng']
    search_fields = ['title']


class ImageAdmin(admin.ModelAdmin):
  list_display = ('place', 'image')
