from django.db import models
from django.utils import timezone


class Album(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField(default=5.99)
    description = models.TextField()
    releaseDate = models.DateField()
    runtime_minutes = models.IntegerField(default=0)
    runtime_seconds = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.releaseDate.year})"

    def is_released(self):
        return self.releaseDate <= timezone.now()

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "releaseDate": {
                "year": self.releaseDate.year,
                "month": self.releaseDate.month,
                "day": self.releaseDate.day
            },
            "runtime": {
                "minutes": self.runtime_minutes,
                "seconds": self.runtime_seconds
            },
            "price": self.price,
            "trackIDs": [t.id for t in self.track_set.all()],
            "description": self.description
        }


class Track(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField(default=0.99)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    runtime_minutes = models.IntegerField(default=0)
    runtime_seconds = models.IntegerField(default=0)
    #file = models.FileField()

    def __str__(self):
        return f"{self.title} ({self.album.title})"

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "runtime": {
                "minutes": self.runtime_minutes,
                "seconds": self.runtime_seconds
            },
            "albumId": self.album.id,
            "albumTitle": self.album.title
        }
