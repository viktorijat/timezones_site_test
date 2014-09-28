from zonesapp.models import UserEntry
from django.http import HttpResponse
import json as simplejson
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from zonesapp.get_entry_list import get_all_entries_list
from django.http import QueryDict
from django.core.exceptions import ValidationError
from zonesapp.utils import *


@csrf_exempt
@basic_http_auth
def edit_by_id(request, pk):

    if request.user.id:

        if request.method == "UPDATE" or request.method == "PUT":

            put = QueryDict(request.body)
            entry_name = str(put.get('entry_name'))
            city_name = str(put.get('city_name'))
            offset = str(put.get('offset'))

            if entry_name is not "" and city_name is not "" and offset is not "":

                try:
                    entry = UserEntry.objects.get(pk=pk)
                    entry.entry_name = entry_name
                    entry.city_name = city_name
                    entry.gmt_offset_display = put.get('offset')

                    try:
                        entry.full_clean()


                    except ValidationError as e:

                        line = ""
                        for key, value in e.message_dict.items():
                            row = ":".join([key, str(value[0])])
                            if line == "":
                                line = row
                            else:
                                line = "\n".join([line, row])

                        response = {'success': False, 'errors': line}

                        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=400)


                    entry.save()
                    response = {'success': True}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=200)

                except UserEntry.DoesNotExist:

                    response = {'success': False}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=404)


        else:
            response = {'note': "method not allowed"}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)

    else:
        response = {'note': "unauthorised"}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=401)

