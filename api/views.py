from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404


# Create your views here.
from .models import Track, Album


def tracks(request):
    q = Track.objects.all()
    body = [track.to_json() for track in q]
    print(body)
    return JsonResponse(body, safe=False)


def track(request, id):
    q = get_object_or_404(Track, pk=id)
    body = q.to_json()
    print(body)
    return JsonResponse(body)


def albums(request):
    q = Album.objects.all()
    body = [album.to_json() for album in q]
    print(body)
    return JsonResponse(body, safe=False)


def album(request, id):
    q = get_object_or_404(Album, pk=id)
    body = q.to_json()
    print(body)
    return JsonResponse(body)
