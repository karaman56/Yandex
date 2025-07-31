from django.contrib import admin
from .models import Place, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview', 'position')

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Превью'

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    search_fields = ['title']
    list_display = ('title',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'position', 'image_preview')
    readonly_fields = ('image_preview',)
    list_filter = ('place',)
    raw_id_fields = ('place',)

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Превью'
