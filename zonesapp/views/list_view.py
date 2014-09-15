import json
from django.views import generic
from django.utils import timezone
from zonesapp.models import UserEntry, Timezones
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from zonesapp.get_entry_list import get_all_entries_list


@csrf_exempt
def entry_list(request):

    if request.method == 'GET':

        current_user = request.user
        print "current_user", current_user
        current_user_id = current_user.id
        query = request.GET.get('query', None)
        if query:
            entries = UserEntry.objects.filter(entry_name__contains=query, user=current_user_id)
        else:
            entries = UserEntry.objects.filter(user=current_user_id)

        all_list = get_all_entries_list(entries)
        if all_list is not False:
            response = {'success': True, 'entry_list': all_list}
            return HttpResponse(json.dumps(response), content_type='application/json', status=201)

        else:
            response = {'success': False, 'entry_list': "not found entries to show, status is 401"}
            return HttpResponse(json.dumps(response), content_type='application/json', status=401)

    else:
        response = {'success': False, 'entry_list': "method not allowed"}
        return HttpResponse(json.dumps(response), content_type='application/json', status=405)




#rest api
#http://www.django-rest-framework.org/api-guide/filtering

'''
class EntryListView(generic.ListView):

    model = UserEntry
    template_name = 'entry_list.html'
    paginate_by = '5'
    context_object_name = 'user_entries'
    #queryset = UserEntry.objects.all()

    def get_queryset(self):

        e_name = self.kwargs['entry_name']#self.request.GET.get('entry_name')
        if e_name:
            entries = UserEntry.objects.filter(entry_name__contains=e_name)
        else:
            entries = UserEntry.objects.all()

        return entries
        #data = serializers.serialize("json", self.get_queryset())#serializers.serialize('entries', entries)
        #response = {'entries': data}  #timzones': serializers.serialize('json', entries)}
        #return HttpResponse(json.dumps(data), content_type='application/json', status=200)
'''



