import json
import datetime
from zonesapp.models import UserEntry
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from zonesapp.utils import *


@csrf_exempt
@logged_in_or_basicauth()
@basic_http_auth
def entry_list(request):


    if request.user.id:

        #print "USERNAME", request.user.username
        #print request.username

        if request.method == 'GET':

            current_user = request.user
            current_user_id = current_user.id
            query = request.GET.get('query', None)
            if query:
                entries = UserEntry.objects.filter(entry_name__contains=query, user=current_user_id)
            else:
                entries = UserEntry.objects.filter(user=current_user_id)


            data = serializers.serialize("json", entries, fields=('pk', 'entry_name', 'city_name',
                                                                  'user', 'gmt_offset_display'))

            if entries:

                return HttpResponse(data, content_type='application/json', status=200)

            else:
                data = serializers.serialize("json", [])
                return HttpResponse(data, content_type='application/json', status=404)

        else:
            response = {'success': False, 'entry_list': "method not allowed"}
            return HttpResponse(json.dumps(response), content_type='application/json', status=405)

    else:
        response = {'success': False}
        return HttpResponse(json.dumps(response), content_type='application/json', status=401)



@csrf_exempt
@basic_http_auth
def get_current_time(request, pk):


    if request.user.id:

        if request.method == 'GET':

            try:
                entry = UserEntry.objects.get(pk=pk)
                obj_time = datetime.timedelta(hours=entry.gmt_offset_display.hour, minutes=entry.gmt_offset_display.minute)
                now = datetime.datetime.now()
                current_time = (now + obj_time).strftime('%Y-%m-%d %H:%M:%S %Z%z')
                return HttpResponse(json.dumps(current_time), content_type='application/json', status=200)
            except UserEntry.DoesNotExist:
                return HttpResponse(json.dumps(''), content_type='application/json', status=404)

        else:
            response = {'success': False, 'note': "method not allowed"}
            return HttpResponse(json.dumps(response), content_type='application/json', status=405)

    else:
        response = {'success': False}
        return HttpResponse(json.dumps(response), content_type='application/json', status=401)




