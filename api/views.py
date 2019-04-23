from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

import json
import subprocess

# Create your views here.
from api.song_delivery import send_song
from .models import *


def tracks(request):
    """
    :url: api/tracks
    :methods: GET
    :return:
    200 - JSON Array of all tracks
    """
    q = Track.objects.all()
    body = [track.to_json() for track in q]
    return JsonResponse(body, safe=False)


def tracks_top(request):
    """
    :url: api/tracks/top
    :methods: GET
    :return:
    200 - JSON list of the top 10 tracks by total downloads.
    """
    qs = Purchase.objects.values('track_id') \
             .order_by('track_id') \
             .annotate(count=Count('track_id')) \
        [:10]

    body = [q['track_id'] for q in qs]
    return JsonResponse(body, safe=False)


def track(request, id):
    """
    :url: api/tracks/<id>
    :methods: GET
    :param id: ID of the track to fetch
    :return:
    200 - JSON Object representing the track info.
    404 - If no such track exists.
    """
    q = get_object_or_404(Track, pk=id)
    body = q.to_json()
    return JsonResponse(body)


def albums(request):
    """
    :url: api/albums
    :methods: GET
    :return:
    200 - JSON Array of all the albums
    """
    q = Album.objects.all()
    body = [album.to_json() for album in q]
    return JsonResponse(body, safe=False)


def album(request, id):
    """
    :url: api/albums/<id>
    :methods: GET
    :param id: ID of the album to fetch
    :return:
    200 - JSON Object representing the album info.
    404 - If no such album exists.
    """
    q = get_object_or_404(Album, pk=id)
    body = q.to_json()
    return JsonResponse(body)


@csrf_exempt
def customer_new(request):
    """
    :url: api/customers/new
    :methods: POST
    :post: { email: str, walletid: str }
    :return:
    200 - If a customer with the provided email and walletid already exists, along with their internal ID.
    201 - If no such customer exists, indicates that a new user has been created and returns their ID.
    400 - JSON encoding error
    """
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
    purchases = {purchase.track.id for customer in customers for purchase in customer.purchase_set.all()}
    return JsonResponse(list(purchases), safe=False)


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

        purchases = []
        for trackid in data["trackIds"]:
            purchase = Purchase(buyer_id=id, track_id=trackid, status="unfufilled")
            purchase.save()
            purchases.append(purchase)

        #purchases = [Purchase(buyer_id=id, track_id=trackid, status="unfufilled") for trackid in data["trackIds"]]
        #Purchase.objects.bulk_create(purchases)

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


def send_songs(request, purchaseid: int):
    purchase = get_object_or_404(Purchase, pk=purchaseid)
    if purchase.status != "unfufilled":
        return HttpResponse("Purchase already fufilled", status=400)

    link = send_song(purchase)
    return HttpResponse(link)
