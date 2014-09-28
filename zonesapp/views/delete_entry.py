from zonesapp.models import UserEntry
from django.http import HttpResponse
import json as simplejson
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from zonesapp.utils import *


@csrf_exempt
@basic_http_auth
def delete_by_id(request, pk):

    if request.user.id:

        if request.method == "DELETE":

            #put = QueryDict(request.body)
            #description = put.get('id')
            try:
                entry = UserEntry.objects.get(pk=pk).delete()
                response = {'note': "deleted"}
                return HttpResponse(simplejson.dumps(response), content_type='application/json', status=200)

            except UserEntry.DoesNotExist:
                response = {'note': "this entry does not exist"}
                return HttpResponse(simplejson.dumps(response), content_type='application/json', status=404)
        else:
            response = {'note': "method not allowed"}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)

    else:
        response = {'note': "unauthorised"}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=401)

