from zonesapp.models import Timezones, UserEntry
import json as simplejson
from django.contrib.auth.models import User
from django.http import HttpResponse
from geopy import geocoders
from django.views.decorators.csrf import csrf_exempt
from zonesapp.all_cities import get_city_info
from django.http import QueryDict
from zonesapp.get_entry_list import get_all_entries_list



@csrf_exempt
def check_city(request):

    print "REQUEST", request

    if request.method == "POST":

        put = QueryDict(request.body)
        city = put.get('city_name')
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

            response = {'success': True, 'entry_list': "this city has no info"}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=200)

    else:
        response = {'success': False, 'entry_list': "method not allowed"}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)


@csrf_exempt
def submit_entry(request):

    if request.method == "PUT":

        put = QueryDict(request.body)
        city = put.get('city_name')
        city_name = str(city)


        g = geocoders.GoogleV3()
        try:
            place, (lat, lng) = g.geocode(city_name)
        except:
            place = city_name
            lat = 0
            lng = 0

        diff = get_city_info(str(city))

        current_user = request.user
        #current_user_id = current_user.id
        new_entry = UserEntry(
            entry_name=str(put.get('entry_name')),
            city_name=city_name,
            user=User.objects.get(username=current_user),
            gmt_offset_display=str(put.get('gmt_offset')),
        )
        new_entry.save()
        current_user = request.user
        current_user_id = current_user.id
        entries = UserEntry.objects.filter(user=current_user_id)
        if diff is not False:
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
        else:
            pass

        all_list = get_all_entries_list(entries)
        if all_list is not False:
            response = {'success': True, 'entry_list': all_list}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=201)

        else:
            response = {'success': False, 'entry_list': "not found entries to show, status is 401"}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=401)

    else:
        response = {'success': False, 'entry_list': "method not allowed"}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)