from django.db import models
from django.db import models


class Place(models.Model):
  title = models.CharField("Название места", max_length=255)
  description_short = models.TextField("Краткое описание")
  description_long = models.TextField("Подробное описание")
  lat = models.FloatField("Широта")
  lng = models.FloatField("Долгота")

  def __str__(self):
    return self.title


class Image(models.Model):
  place = models.ForeignKey(
    Place,
    on_delete=models.CASCADE,
    related_name='images',
    verbose_name="Место"
  )
  image = models.ImageField("Изображение", upload_to='places/')
  position = models.PositiveIntegerField("Позиция", default=0)

  class Meta:
    ordering = ['position']

  def __str__(self):
    return f"Изображение для {self.place.title}"

