from django.db import models
from django.contrib.auth.models import User
import datetime

class Timezones(models.Model):

    timezone_name = models.TextField(max_length=500)
    offset = models.TextField(max_length=500)
    local_time = models.TextField(max_length=500)
    longitude = models.FloatField()
    latitude = models.FloatField()


class UserEntry(models.Model):

    entry_name = models.TextField(max_length=500)
    city_name = models.TextField(max_length=500)
    user = models.ForeignKey(User)
    gmt_offset_display = models.TimeField(default="00:00:00")
    tmz = models.ManyToManyField(Timezones)
