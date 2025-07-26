from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=255)
    description_short = models.TextField(blank=True, null=True)
    description_long = HTMLField(blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()


    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='places/')
    position = models.PositiveIntegerField("Позиция", default=0, db_index=True)


    class Meta:
        ordering = ['position']


    def __str__(self):
        return f"Image for {self.place.title}"
