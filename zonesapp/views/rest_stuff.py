from rest_framework.renderers import JSONRenderer
from django.shortcuts import *
from zonesapp.models import Timezones, UserEntry
from zonesapp.serializers import TimezonesSerializer, UserEntrySerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


class JSONResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def timezones_list(request):

    if request.method == 'GET':
        zones = Timezones.objects.all()
        serializer = TimezonesSerializer(zones, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TimezonesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def user_entries_list(request):

    if request.method == 'GET':
        entries = UserEntry.objects.all()
        serializer = UserEntrySerializer(entries, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserEntrySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)