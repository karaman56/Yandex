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
