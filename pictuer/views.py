import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from model.models import *
from model.configuration import *
import uuid


@csrf_protect
def upload_image(request, id):
    if request.method == 'GET':

        return render(request, 'pictuer.html', {'id': id})
    else:

        return HttpResponse("Only GET requests are supported for this view.")


@csrf_protect
def process_image(request):
    if request.method == 'POST':
        global pic
        global user

        try:
            d = json.loads(request.body.decode('utf-8'))
            pic = d['picture']
            user = d['id']
        except KeyError as e:

            new_error = Error(f"{str(uuid.uuid4())}")
            new_error.create_date = NOW
            new_error.id = user
            new_error.save()
            return HttpResponse("key error")

        new_picture = Picture(f"{str(uuid.uuid4())}")
        new_picture.create_date = NOW_GMT
        new_picture.id = user
        new_picture.status = "False"
        new_picture.picture = pic
        new_picture.save()

        return HttpResponse("Successful")

    else:
        return HttpResponse("Only POST requests are supported for this view.")


def send_picture(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if request.method == "GET" and auth_header:
        if auth_header == token:
            lis = []
            for picture in Picture.A():
                if picture.status == "FALSE":
                    lis.append({
                        "id": picture.id,
                        "picture": picture.picture
                    })
                    picture.status = "TRUE"
                    picture.save()

            return JsonResponse(lis, safe=False)
        else:
            return HttpResponse('Unauther', status=401)
    else:
        return HttpResponse("Token not found", status=400)
