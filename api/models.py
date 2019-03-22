from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField(default=5.99)
    description = models.TextField()
    releaseDate = models.DateField()
    runtime_seconds = models.IntegerField(default=0)
    runtime_minutes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.releaseDate.year})"


class Track(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField(default=0.99)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    runtime_seconds = models.IntegerField(default=0)
    runtime_minutes = models.IntegerField(default=0)
    #file = models.FileField()

    def __str__(self):
        return f"{self.title} ({self.album.title})"
