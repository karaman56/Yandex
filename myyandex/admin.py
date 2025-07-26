from django.contrib import admin
from .models import Place, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    fields = ('image', 'position')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    search_fields = ['title']
    list_display = ('title',)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('place', 'position')
