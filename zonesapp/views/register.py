import json as simplejson
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register_form_event(request):

    if request.method == "POST":

        name = str(request.POST["name"])
        email = str(request.POST['email'])
        passw = request.POST['password']
        passw1 = request.POST['password1']

        if name is not "" and email is not "" and passw is not "" and passw1 is not "":


            try:
                user = User.objects.get(username=name)
                if user:
                    response = {'success': False, 'note': "this user exists"}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=409)

            except User.DoesNotExist:

                if passw == passw1:
                    user = User.objects.create_user(
                        username=name,
                        email=email,
                        password=passw,
                    )

                    try:
                        user.full_clean()
                        user.save()
                        user = authenticate(username=request.POST['name'], password=request.POST['password'])
                        login(request, user)
                        response = {'success': True, 'note': "user is logged in"}
                        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=201)

                    except IntegrityError:
                        response = {'success': True, 'name': request.POST["name"],
                                    'note': "conflict, user already exists"}
                        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=409)

                else:
                    response = {'note': "bad request, please modify data"}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=400)

        else:

            response = {'note': "bad request, no data provided"}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=400)

    else:
        response = {'success': False, 'note': "method not allowed"}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)