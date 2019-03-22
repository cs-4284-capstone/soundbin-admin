from django.db import models


# Create your models here.
class Track(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    albumId = models.IntegerField()
    albumTitle = models.CharField(max_length=200)
    runtimeSeconds = models.IntegerField()
    runtimeMinutes = models.IntegerField()
