from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import json

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

@csrf_exempt
def associate(request):
    if request.method != 'POST':
        print('Invalid non-post call to associate')
        return HttpResponse('Invalid request type, must be post', status=400)

    data = json.loads(request.body)
    print(f'Recieved data: (wallet:{data["walletid"]}, email:{data["email"]})')

    if True:    # TODO: attempt to add to database
        return HttpResponse('Wallet and email associated', status=200)
    else:
        return HttpResponse('Unknown error', status=500)
