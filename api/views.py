from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import json

# Create your views here.
from .models import Track, Album, Customer, customer_from_json


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
def customer_new(request):
    if request.method != 'POST':
        return HttpResponse('Invalid request type, must be POST', status=400)

    try:
        data = json.loads(request.body)
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
