from zonesapp.models import UserEntry, Timezones
from zonesapp.serializers import UserEntrySerializer, TimezonesSerializer, UserSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import status
import django_filters
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response


'''
#CLASS USER ENTRY
class EntryFilter(django_filters.FilterSet):

    class Meta:
        model = UserEntry
        fields = ['entry_name']

'''


#CLASS USER ENTRY
class EntryFilter(django_filters.FilterSet):

    class Meta:
        model = UserEntry
        fields = ['user', 'entry_name']



class UserEntryListRest(generics.ListAPIView):

    serializer_class = UserEntrySerializer
    queryset = UserEntry.objects.all()
    #filter_fields = ('entry_name')
    filter_class = EntryFilter



class UserEntryListRestAdd(generics.ListCreateAPIView):

    serializer_class = UserEntrySerializer
    queryset = UserEntry.objects.all()


class UserEntryListRestEdit(generics.UpdateAPIView):

    serializer_class = UserEntrySerializer
    queryset = UserEntry.objects.all()



class UserEntryListRestDelete(generics.DestroyAPIView):

    model = UserEntry
    serializer_class = UserEntrySerializer



#CLASS TIMEZONE
class TimezoneFilter(django_filters.FilterSet):

    class Meta:
        model = Timezones
        fields = ['timezone_name']


class TimezoneListRest(generics.ListAPIView):

    serializer_class = TimezonesSerializer
    queryset = Timezones.objects.all()
    filter_class = TimezoneFilter


class TimezoneListRestAdd(generics.ListCreateAPIView):

    serializer_class = TimezonesSerializer
    queryset = Timezones.objects.all()



class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet that for listing or retrieving users.
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)




#CLASS AUTH USER
class UserFilter(django_filters.FilterSet):

    class Meta:
        model = User
        fields = ['username']


class UserListRest(generics.ListAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_class = UserFilter


class UserListRestAdd(generics.ListCreateAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListRestEdit(generics.UpdateAPIView):

    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListRestDelete(generics.DestroyAPIView):

    model = User
    serializer_class = UserSerializer
    #queryset = User.objects.all()
