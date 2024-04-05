from django.urls import path

from pictuer.views import *

urlpatterns = [
    path('<int:id>',upload_image,name='upload_image'),
    path('get_image',process_image,name='process_image'),
]