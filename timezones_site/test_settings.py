from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ":memory:",
    },
}


#export PYTHONPATH=$PYTHONPATH:/home/krste/timezones_site
#export DJANGO_SETTINGS_MODULE=timezones_site.test_settings
