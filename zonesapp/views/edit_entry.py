from zonesapp.models import UserEntry
from django.http import HttpResponse
import json as simplejson
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from zonesapp.get_entry_list import get_all_entries_list
from django.http import QueryDict



@csrf_exempt
def edit_by_id(request):

    if request.method == "UPDATE" or request.method == "PUT":

        put = QueryDict(request.body)
        entry_id = str(put.get('entry_id'))
        entry_name = str(put.get('entry_name'))
        city_name = str(put.get('city_name'))
        offset = str(put.get('offset'))

        if entry_id is not "" and entry_name is not "" and city_name is not "" and offset is not "":

            print entry_id, entry_name, city_name, offset

            entry = UserEntry.objects.get(pk=entry_id)

            if entry:

                entry.entry_name = entry_name
                entry.city_name = city_name
                entry.gmt_offset_display = put.get('offset')
                entry.save()


                current_user = request.user
                print "current_user", current_user
                current_user_id = current_user.id
                entries = UserEntry.objects.filter(user=current_user_id)

                all_list = get_all_entries_list(entries)

                if all_list is not False:

                    response = {'success': True, 'entry_list': all_list}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=200)

                else:
                    response = {'success': False, 'entry_list': "no content to show"}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=204)

            else:

                entries = UserEntry.objects.all()
                all_list = get_all_entries_list(entries)

                if all_list is not False:

                    response = {'success': True, 'entry_list': all_list}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=404)

                else:
                    response = {'success': False, 'entry_list': "no content to show"}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=204)

    else:
        response = {'note': "method not allowed"}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)