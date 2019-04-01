from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

import json
import subprocess

# Create your views here.
from .models import *


def tracks(request):
    q = Track.objects.all()
    body = [track.to_json() for track in q]
    return JsonResponse(body, safe=False)


def tracks_top(request):
    qs = Purchase.objects.values('track_id')\
        .order_by('track_id')\
        .annotate(count=Count('track_id'))
    body = [q['track_id'] for q in qs]
    return JsonResponse(body, safe=False)


def track(request, id):
    q = get_object_or_404(Track, pk=id)
    body = q.to_json()
    return JsonResponse(body)


def albums(request):
    q = Album.objects.all()
    body = [album.to_json() for album in q]
    return JsonResponse(body, safe=False)


def album(request, id):
    q = get_object_or_404(Album, pk=id)
    body = q.to_json()
    return JsonResponse(body)


@csrf_exempt
def customer_new(request):
    if request.method == 'OPTIONS':
        return HttpResponse("", status=200)
    if request.method != 'POST':
        return HttpResponse('Invalid request type, must be POST', status=405)

    try:
        data = json.loads(request.body)
        preexisting = Customer.objects.filter(email=data["email"], walletid=data["walletid"]).first()
        if preexisting is not None:
            ret = {
                "result": "already_created",
                "body": preexisting.to_json()
            }
            return JsonResponse(ret, status=200)

        customer = customer_from_json(data)
        customer.save()
    except json.decoder.JSONDecodeError:
        error = {
            "result": "error",
            "type": "JSONDecoderError",
            "message": "Request contained improperly-formatted JSON.",
            "status": 400
        }
        return JsonResponse(error, status=error['status'])
    except KeyError:
        error = {
            "result": "error",
            "type": "KeyError",
            "message": "The following keys are required: [email, walletid]",
            "status": 400
        }
        return JsonResponse(error, status=error['status'])
    else:
        ret = {
            "result": "ok",
            "body": customer.to_json()
        }
        return JsonResponse(ret, status=201)


def customer_purchases(request, id):
    # TODO: validation probably needed here
    customer = get_object_or_404(Customer, pk=id)
    purchases = customer.purchase_set.all()
    return JsonResponse([p.to_json() for p in purchases], safe=False)


def customer_email_purchases(request, email: str):
    customers = Customer.objects.filter(email=email)
    purchases = [purchase.track.to_json() for customer in customers for purchase in customer.purchase_set.all()]
    return JsonResponse(purchases, safe=False)


@csrf_exempt
def customer_purchase_new(request, id):
    """
    TODO: better CSRF protection...
    TODO: album bundle discounts...
    TODO: integrate with django users?
    {
        email: string,
        trackIds: TrackID[],
    }
    """
    if request.method == 'OPTIONS':
        return HttpResponse("", status=200)
    if request.method != 'POST':
        return HttpResponse('Invalid request type, must be POST', status=405)

    customer = get_object_or_404(Customer, pk=id)
    try:
        data = json.loads(request.body)

        if data['email'] != customer.email:
            error = {
                "result": "error",
                "type": "AuthError",
                "message": "Not Authorized.",
                "status": 401
            }
            return JsonResponse(error, status=error['status'])

        if len(data["trackIds"]) == 0:
            raise KeyError

        purchases = [Purchase(buyer_id=id, track_id=trackid, status="unfufilled") for trackid in data["trackIds"]]
        Purchase.objects.bulk_create(purchases)

    except json.decoder.JSONDecodeError:
        error = {
            "result": "error",
            "type": "JSONDecoderError",
            "message": "Request contained improperly-formatted JSON.",
            "status": 400
        }
        return JsonResponse(error, status=error['status'])
    except KeyError:
        error = {
            "result": "error",
            "type": "KeyError",
            "message": "The following keys are required: [email, walletid]",
            "status": 400
        }
        return JsonResponse(error, status=error['status'])
    else:
        ret = {
            "result": "ok",
            "body": [p.to_json() for p in purchases]
        }

        return JsonResponse(ret, status=201, safe=False)

@csrf_exempt
def add_transaction(request, wallet_id, purchases):
    """
    Process the purchase of tracks/albums.

    Songs format is a list of comma separated tracks and comma separated, with a
    pipe as a divider.

    Example: "1,2,3|4,5,6" where 1,2,3 are purchased tracks and 4,5,6 are
    purchased albums.

    This function will currently send an email automatically, but eventually
    it will aggregate transactions and group them into one email.
    """
    # email to send tracks to
    email = Customer.objects.filter(walletid=wallet_id).last().email
    
    songs, albums = purchases.split('|')

    songs = [int(song) for song in songs.split(',')]
    albums = [int(album) for album in albums.split(',')]

    print(songs)
    print(albums)

    song_titles = []
    for song in songs:
        try:
            song_title = Track.objects.get(id=song)
            song_titles.append(song_title.title + '.mp3')
        except ObjectDoesNotExist:
            print(f'song of id: {song} does not exist in db')

    print(song_titles)

    args = ["./api/song_emailer/send_song.py", email, '-s', *song_titles]
    process = subprocess.run(args, capture_output=True)
    print(process)
    print(process.stdout)
    return HttpResponse()

def send_songs(request):
    pass
