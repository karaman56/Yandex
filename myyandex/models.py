from django.db import models
from tinymce.models import HTMLField

class Place(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название места'
    )
    short_description = models.TextField(
        blank=True,
        verbose_name='Краткое описание',
        default=''
    )
    long_description = HTMLField(
        blank=True,
        verbose_name='Подробное описание',
        default=''
    )
    lat = models.FloatField(
        verbose_name='Широта'
    )
    lng = models.FloatField(
        verbose_name='Долгота'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'


class Image(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
    )
    image = models.ImageField(
        upload_to='places/',
        verbose_name='Изображение'
    )
    position = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name='Позиция'
    )

    class Meta:
        ordering = ['position']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f"Изображение для {self.place.title}"
