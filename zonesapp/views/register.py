import json as simplejson
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from django.core.exceptions import ValidationError


@csrf_exempt
def register_form_event(request):

    if request.method == "POST":

        #POSTER
        #name=vikk&email=asd@asd.com&password=vikk&password1=vikk
        #content type: application/x-www-form-urlencoded


        post_dict = QueryDict(request.body)
        #print "post dict", post_dict

        name = post_dict.get('name')
        email = post_dict.get('email')
        passw = post_dict.get('password')
        passw1 = post_dict.get('password1')



        #name = str(request.POST["name"])
        #email = str(request.POST['email'])
        #passw = request.POST['password']
        #passw1 = request.POST['password1']

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
                    success = True
                    obj = user

                except ValidationError as e:

                    success = False
                    obj = e

                    usr = User.objects.get(username=name)
                    if usr:
                        usr.delete()

                print success, obj

                if success == False:

                    line = ""
                    for key, value in obj.message_dict.items():
                        row = ":".join([key, str(value[0])])
                        if line == "":
                            line = row
                        else:
                            line = "\n".join([line, row])

                    response = {'success': False, 'errors': line}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=400)

                else:
                    user.save()
                    user = authenticate(username=name, password=passw)
                    login(request, user)
                    response = {'success': True, 'note': "user is logged in"}
                    return HttpResponse(simplejson.dumps(response), content_type='application/json', status=201)


            else:
                response = {'success': False, 'errors': "passwords don't match"}
                return HttpResponse(simplejson.dumps(response), content_type='application/json', status=400)

    else:
        response = {'success': False, 'note': "method not allowed"}
        return HttpResponse(simplejson.dumps(response), content_type='application/json', status=405)


'''
else:

            response = {'note': "bad request, no data provided"}
            return HttpResponse(simplejson.dumps(response), content_type='application/json', status=400)
'''