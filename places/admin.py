from django.contrib import admin
from .models import Place, Image
from django.utils.html import format_html


class ImageInline(admin.TabularInline):
  model = Image
  extra = 3
  fields = ('image', 'position', 'preview')
  readonly_fields = ('preview',)

  def preview(self, obj):
    if obj.image:
      return format_html('<img src="{}" height="150">', obj.image.url)
    return "Превью"


class PlaceAdmin(admin.ModelAdmin):
  inlines = [ImageInline]
  list_display = ['title', 'lat', 'lng']
  search_fields = ['title']


class ImageAdmin(admin.ModelAdmin):
  list_display = ('place', 'preview')

  def preview(self, obj):
    if obj.image:
      return format_html('<img src="{}" height="50">', obj.image.url)
    return "Нет изображения"



admin.site.register(Place, PlaceAdmin)
admin.site.register(Image, ImageAdmin)
