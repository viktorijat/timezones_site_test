from django.conf.urls import include, url
from django.contrib import admin
import zonesapp.urls


urlpatterns = [
    # Examples:
    # url(r'^$', 'timezones_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('zonesapp.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
