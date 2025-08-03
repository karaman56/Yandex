from django.contrib import admin
from django.utils.html import format_html
from .models import Place, Image


class ImageInline(admin.TabularInline):
  model = Image
  extra = 0
  readonly_fields = ('image_preview',)
  fields = ('position', 'image', 'image_preview')

  def image_preview(self, obj):
    if obj.image:
      return format_html(
        '<img src="{}" style="max-height: 200px; width: auto; object-fit: contain;" />',
        obj.image.url
      )
    return "-"

  image_preview.short_description = 'Превью'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
  inlines = [ImageInline]
  search_fields = ['title']
  list_display = ('title', 'short_description_preview')
  readonly_fields = ('images_preview',)
  fieldsets = (
    (None, {
      'fields': ('title', 'short_description', 'long_description')
    }),
    ('Координаты', {
      'fields': ('lat', 'lng')
    }),
    ('Превью', {
      'fields': ('images_preview',),
      'classes': ('collapse',)
    })
  )

  def short_description_preview(self, obj):
    return obj.short_description[:100] + '...' if obj.short_description else "-"

  short_description_preview.short_description = 'Краткое описание'

  def images_preview(self, obj):
    images = obj.images.all()
    previews = []
    for img in images:
      previews.append(
        f'<div style="float: left; margin-right: 10px;">'
        f'<img src="{img.image.url}" style="max-height: 150px; width: auto; margin-bottom: 5px;" />'
        f'<p style="text-align: center;">Позиция: {img.position}</p>'
        f'</div>'
      )
    return format_html(''.join(previews)) if previews else "-"

  images_preview.short_description = 'Превью изображений'
  images_preview.allow_tags = True


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
  list_display = ('place_title', 'position', 'image_preview')
  readonly_fields = ('image_preview',)
  list_filter = ('place',)
  raw_id_fields = ('place',)
  fields = ('place', 'position', 'image', 'image_preview')

  def place_title(self, obj):
    return obj.place.title

  place_title.short_description = 'Место'

  def image_preview(self, obj):
    if obj.image:
      return format_html(
        '<img src="{}" style="max-height: 200px; width: auto; object-fit: contain;" />',
        obj.image.url
      )
    return "-"

  image_preview.short_description = 'Превью'
