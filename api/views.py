from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.
from .models import *


def tracks(request):
    q = Track.objects.all()
    body = [track.to_json() for track in q]
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
    purchases = customer.purchase_set
    return JsonResponse([p.to_json() for p in purchases], safe=False)


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
