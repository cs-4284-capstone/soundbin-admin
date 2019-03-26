from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.
from .models import Track, Album, User


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
    association = User(wallet_id=data['walletid'], email=data['email'])
    print(f'Recieved data: (wallet:{data["walletid"]}, email:{data["email"]})')

    association.save()
    print(association)
    return HttpResponse('Wallet and email associated', status=200)

@csrf_exempt
def add_transaction(request, wallet_id, songs):
    """
    Process the purchase of songs/albums.

    Songs format is a list of comma separated songs and comma separated, with a
    pipe as a divider.

    Example: "1,2,3|4,5,6" where 1,2,3 are purchased songs and 4,5,6 are
    purchased albums.

    This function will currently send an email automatically, but eventually
    it will aggregate transactions and group them into one email.
    """
    pass

def send_songs(request):
    pass
