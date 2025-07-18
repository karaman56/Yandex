from django.contrib import admin
from .models import Place, Image
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase

class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 3
    fields = ('image', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="150">', obj.image.url)
        return "Превью"

# Наследуем PlaceAdmin от SortableAdminBase
@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['title', 'lat', 'lng']
    search_fields = ['title']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'place', 'position')
    list_editable = ('position',)
