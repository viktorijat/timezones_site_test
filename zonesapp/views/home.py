from django.shortcuts import *
from django.shortcuts import render_to_response


def home(request):
    request.session.set_test_cookie()
    return render_to_response('index.html', locals(),
                              context_instance=RequestContext(request))


def profile(request):
    return render_to_response('index.html', locals(),
                              context_instance=RequestContext(request))



