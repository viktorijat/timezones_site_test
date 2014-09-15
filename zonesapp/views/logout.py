import json as simplejson
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def logout_event(request):

    if request.method == "POST":

        if request.user.is_authenticated():
            print '2'
            logout(request)
            data = {'success': True, 'note': "user is logged out"}
            return HttpResponse(simplejson.dumps(data), content_type='application/json', status=200)

        else:
            print '3'
            data = {'success': False, 'note': "user isnt logged out"}
            return HttpResponse(simplejson.dumps(data), content_type='application/json', status=401)

    else:
        response = {'success': False, 'note': "method not allowed"}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)