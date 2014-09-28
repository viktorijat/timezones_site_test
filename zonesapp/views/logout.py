import json as simplejson
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from zonesapp.utils import *
from django.contrib.auth.models import AnonymousUser


@csrf_exempt
@basic_http_auth
def logout_event(request):

    if request.user.id:

        if request.method == "POST":

            if request.user.is_authenticated():
                logout(request)
                request.session.flush()
                request.user = AnonymousUser()
                data = {'success': True, 'note': "user is logged out"}
                return HttpResponse(simplejson.dumps(data), content_type='application/json', status=200)

            else:
                data = {'success': False, 'note': "user isnt logged out"}
                return HttpResponse(simplejson.dumps(data), content_type='application/json', status=401)

        else:
            response = {'success': False, 'note': "method not allowed"}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)

    else:
        response = {'success': False}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=401)

