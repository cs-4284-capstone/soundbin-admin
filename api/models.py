from django.db import models
from django.utils import timezone


def art_path(album, filename: str) -> str:
    return f"uploads/albumart/{album.id}.png"


def track_path(track, filename: str) -> str:
    return f"uploads/tracks/{track.album_id}/{track.id}.mp3"


class Album(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField(default=5.99)
    description = models.TextField()
    releaseDate = models.DateField()
    runtime_minutes = models.IntegerField(default=0)
    runtime_seconds = models.IntegerField(default=0)

    album_art = models.ImageField(default="uploads/albumaart/default.png", upload_to=art_path)

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

    mp3 = models.FileField(default="uploads/songs/null.mp3", upload_to=track_path)

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


class Customer(models.Model):
    email = models.EmailField()   # TODO: change to EmailField
    walletid = models.CharField(max_length=32)  # TODO: i forgot how long this was

    def __str__(self):
        return self.email + "/" + self.walletid

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "walletid": self.walletid
        }


def customer_from_json(json_dict):
    return Customer(email=json_dict['email'], walletid=json_dict['walletid'])


class Purchase(models.Model):
    buyer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    status = models.CharField(max_length=16)

    def __str__(self):
        return str(self.buyer) + " " + str(self.track)

    def to_json(self):
        return {
            "buyer": self.buyer.to_json(),
            "track": self.track.to_json(),
            "status": self.status
        }
