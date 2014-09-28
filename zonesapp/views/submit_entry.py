from zonesapp.models import Timezones, UserEntry
import json as simplejson
from django.contrib.auth.models import User
from django.http import HttpResponse
from geopy import geocoders
from django.views.decorators.csrf import csrf_exempt
from zonesapp.all_cities import get_city_info
from django.http import QueryDict
from zonesapp.get_entry_list import get_all_entries_list
from django.core.exceptions import ValidationError
from zonesapp.utils import *


@csrf_exempt
@basic_http_auth
def check_city(request):

    if request.user.id:

        if request.method == "GET":

            #city = request.POST.get('query', None)
            city = request.GET.get('query', None)
            print city
            put = QueryDict(request.body)
            #city = put.get('city_name')
            #city = request.POST["city_name"]
            g = geocoders.GoogleV3()
            place, (lat, lng) = g.geocode(city)

            diff = get_city_info(str(city))

            if diff is not False:

                whole_string = " ".join([str(city), "info longitude:", str(lng), "latitude:", str(lat), "\n"])

                for entry in diff:

                    timezone_line = " ".join([city, "is in timezone", entry[2]])
                    local_time = " ".join(["Local time is", entry[1]])
                    difference = " ".join(["Difference to GMT is", entry[0]])

                    line = "\n".join([timezone_line, local_time, difference])

                    whole_string = "\n".join([whole_string, line, "\n"])

                response = {'success': True, 'entry_list': whole_string}
                return HttpResponse(simplejson.dumps(response), content_type='application/json', status=200)

            else:

                response = {'success': True, 'entry_list': str(city) + " has no info"}
                return HttpResponse(simplejson.dumps(response), content_type='application/json', status=200)

        else:
            response = {'success': False, 'entry_list': "method not allowed"}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)
    else:
        response = {'success': False}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=401)



@csrf_exempt
@basic_http_auth
def submit_entry(request):

    if request.user.id:

        if request.method == "PUT":

            put = QueryDict(request.body)
            city = put.get('city_name')
            city_name = str(city)

            new_entry_name = str(put.get('entry_name'))

            try:
                exists = UserEntry.objects.get(entry_name=new_entry_name)
                if exists:
                    response = {'success': False, 'errors': "entry with this name already exists"}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=409)

            except UserEntry.DoesNotExist:

                g = geocoders.GoogleV3()
                try:
                    place, (lat, lng) = g.geocode(city_name)
                except:
                    place = city_name
                    lat = 0
                    lng = 0

                diff = get_city_info(str(city))
                current_user = request.user
                print str(put.get('entry_name')), city_name, User.objects.get(username=current_user), put.get('gmt_offset')
                new_entry = UserEntry(
                    entry_name=str(put.get('entry_name')),
                    city_name=city_name,
                    user=User.objects.get(username=current_user),
                    gmt_offset_display=put.get('gmt_offset'),
                )

                try:
                    new_entry.full_clean()
                except ValidationError as e:

                    line = ""
                    for key, value in e.message_dict.items():
                        row = ":".join([key, str(value[0])])
                        if line == "":
                            line = row
                        else:
                            line = "\n".join([line, row])
                    print line
                    response = {'success': False, 'errors': line}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=400)

                new_entry.save()

                if diff == False:
                    pass
                else:
                    for entry in diff:
                        new_timezone = Timezones(
                            timezone_name=entry[2],
                            offset=entry[0],
                            local_time=entry[1],
                            longitude=lng,
                            latitude=lat,
                        )

                        new_timezone.save()
                        new_entry.tmz.add(new_timezone)

                    new_entry.save()

                response = {'success': True}
                return HttpResponse(simplejson.dumps(response), content_type='application/json', status=201)


        else:
            response = {'success': False, 'note': "method not allowed"}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)

    else:
        response = {'success': False}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=401)

