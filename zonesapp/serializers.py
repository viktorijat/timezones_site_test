from django.forms import widgets
from rest_framework import serializers
from zonesapp.models import UserEntry, Timezones
from django.contrib.auth.models import User


class TimezonesSerializer(serializers.ModelSerializer):

    pk = serializers.Field()
    timezone_name = serializers.CharField(max_length=500)
    offset = serializers.CharField(max_length=500)
    local_time = serializers.CharField(max_length=500)
    longitude = serializers.CharField(max_length=500)
    latitude = serializers.CharField(max_length=500)

    class Meta:
        model = Timezones
        fields = ('timezone_name', 'offset', 'local_time', 'longitude', 'latitude')

    '''

    def restore_object(self, attrs, instance=None):

        if instance:
            instance.title = attrs.get('timezone_name', instance.timezone_name)
            instance.code = attrs.get('offset', instance.offset)
            instance.linenos = attrs.get('local_time', instance.local_time)
            instance.language = attrs.get('longitude', instance.longitude)
            instance.style = attrs.get('latitude', instance.latitude)
            return instance

        return Timezones(**attrs)
    '''

class UserEntrySerializer(serializers.ModelSerializer):

    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    entry_name = serializers.CharField(required=False, max_length=500)
    city_name = serializers.CharField(required=False, max_length=500)
    user = serializers.GenericForeignKey(User)
    gmt_offset_display = serializers.TimeField(default="00:00:00")

    class Meta:
        model = UserEntry
        fields = ('entry_name', 'city_name', 'user', 'gmt_offset_display')
        lookup_field = 'pk'

    '''
    def restore_object(self, attrs, instance=None):

        if instance:
            instance.entry_name = attrs.get('entry_name', instance.entry_name)
            instance.city_name = attrs.get('city_name', instance.city_name)
            instance.user = attrs.get('user', instance.user)
            instance.gmt_offset_display = attrs.get('gmt_offset_display', instance.gmt_offset_display)
            return instance

        return UserEntry(**attrs)

    '''


class UserSerializer(serializers.ModelSerializer):

    pk = serializers.Field()
    username = serializers.CharField(required=False, max_length=500)
    password = serializers.CharField(required=False, max_length=500)
    email = serializers.CharField(required=False, max_length=500)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def restore_object(self, attrs, instance=None):

        if instance:
            instance.title = attrs.get('username', instance.username)
            instance.code = attrs.get('password', instance.password)
            instance.linenos = attrs.get('email', instance.email)
            return instance

        return User(**attrs)