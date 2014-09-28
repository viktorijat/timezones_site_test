import json as simplejson
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import QueryDict


@csrf_exempt
def log_in_form_event(request):


    # curl -X POST -d "{"name": "viktorijat", "password": "viktorija33"}" -H 'content-type':application/json' http://127.0.0.1:8000/log_in_form_event/

    #POSTER
    #name=viktorijat&password=viktorija33
    #content type: application/x-www-form-urlencoded

    if request.method == "POST":

        post_dict = QueryDict(request.body)
        name = post_dict.get('name')
        password = post_dict.get('password')


        if name != "" and password != "":

            user = authenticate(username=name, password=password)
            if request.method == "POST":
                try:
                    at = User.objects.get(username=name)


                except:
                    at = False

            if at == False:

                response = {'success': False, 'note': "this username does not exist "}
                return HttpResponse(simplejson.dumps(response), content_type='application/json', status=401)
            else:
                try:
                    import base64

                    authtype, auth = request.META['HTTP_AUTHORIZATION'].split(' ')
                    auth = base64.b64decode(auth)
                    print

                    print "============================================="
                    print "HTTP", request.META['HTTP_AUTHORIZATION']
                    username, password = auth.split(':')
                    print username, password
                    print "============================================="
                    request.user = User.objects.get(username=name)
                    login(request, user)
                    response = {'success': True, 'note': "logged in"}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=200)

                except:
                    print "=================BADPASSWORD==============="
                    print name, password
                    response = {'success': False, 'note': "password is bad"}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=401)
        else:

            response = {'note': "bad request, no data provided"}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=400)
    else:
        response = {'success': False, 'note': "method not allowed"}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)


