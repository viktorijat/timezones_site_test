import json as simplejson
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf


@csrf_exempt
def log_in_form_event(request):

    c = {}
    c.update(csrf(request))
    print "c", c

    if request.method == "POST":

        if request.POST['name'] != "" and request.POST["password"] != "":

            user = authenticate(username=request.POST["name"], password=request.POST["password"])
            if request.method == "POST":
                try:
                    at = User.objects.get(username=request.POST["name"])
                except:
                    at = False

            if at == False:
                response = {'success': False, 'note': "this username does not exist"}
                return HttpResponse(simplejson.dumps(response), content_type='application/json', status=401)
            else:
                try:
                    login(request, user)
                    response = {'success': True, 'name': request.POST["name"], 'note': "logged in"}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=200)
                except:
                    response = {'success': False, 'name': request.POST["name"], 'note': "password is bad"}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=401)
        else:

            response = {'note': "bad request, no data provided"}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=400)
    else:
        response = {'success': False, 'note': "method not allowed"}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)


