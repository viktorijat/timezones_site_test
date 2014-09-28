from zonesapp.views import rest_list_views, delete_entry, logout, list_view, home, submit_entry, log_in, register, edit_entry, rest_register
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', home.home, name='home'),

    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #(r'^/$', ListView.as_view(
    #    model=Timezone,
    #)),

    url(r'^log_in_form_event/', log_in.log_in_form_event, name='log_in_form_event'),
    url(r'^register_form_event/', register.register_form_event, name='register_form_event'),
    url(r'^entry_list/$', list_view.entry_list, name='entry_list'),
    url(r'^get_current_time/(?P<pk>.+)/$', list_view.get_current_time, name='get_current_time'),
    url(r'^submit_entry/', submit_entry.submit_entry, name='submit_entry'),
    url(r'^check_city/$', submit_entry.check_city, name='check_city'),
    url(r'^logout_event/', logout.logout_event, name='logout_event'),
    url(r'^delete_by_id/(?P<pk>.+)/$', delete_entry.delete_by_id, name='delete_by_id'),
    url(r'^edit_by_id/(?P<pk>.+)/$', edit_entry.edit_by_id, name='edit_by_id'),

    url('^rest_users/$', rest_list_views.UserListRest.as_view()),
    url('^rest_users_add/$', rest_list_views.UserListRestAdd.as_view()),

    #http://127.0.0.1:8000/rest_users_delete/1/ raboti
    #http://127.0.0.1:8000/rest_users_edit/1/ raboti

    url('^rest_users_edit/(?P<pk>.+)/$', rest_list_views.UserListRestEdit.as_view()),
    url('^rest_users_delete/(?P<pk>.+)/$', rest_list_views.UserListRestDelete.as_view()),

    #login with rest http://127.0.0.1:8000/api-auth/login/
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #register with rest http://127.0.0.1:8000/rest-auth/register/
    url(r'^rest-auth/', include('rest_auth.urls')),

    #rest api for entries list, add entry, filter by entry_name
    #filter: http://127.0.0.1:8000/rest_entries/?entry_name=aaa
    #list: http://127.0.0.1:8000/rest_entries/
    url('^rest_entries/$', rest_list_views.UserEntryListRest.as_view()),
    url('^rest_entries_add/$', rest_list_views.UserEntryListRestAdd.as_view()),
    #http://127.0.0.1:8000/rest_entries_delete/1/ raboti
    url('^rest_entries_delete/(?P<pk>.+)/$', rest_list_views.UserEntryListRestDelete.as_view()),
    #http://127.0.0.1:8000/rest_entries_edit/1/ raboti
    url('^rest_entries_edit/(?P<pk>.+)/$', rest_list_views.UserEntryListRestEdit.as_view()),

    #rest api for timezones list, add timezone, filter by timezone_name
    #filter: http://127.0.0.1:8000/rest_timezones/?timezone_name=aaa
    #list: http://127.0.0.1:8000/rest_timezones/
    url('^rest_timezones/$', rest_list_views.TimezoneListRest.as_view()),
    url('^rest_timezones_add/$', rest_list_views.TimezoneListRestAdd.as_view()),


    url('^accounts/profile/$', rest_register.ExampleView.as_view()),




    #url('^rest_entries/(?P<entry_name>.+)/$', rest_list_views.UserEntryListRestFilter.as_view()),

    #url('^rest_timezones/$', rest_list_views.TimezonesListRest.as_view()),
    #url('^rest_timezones/(?P<timezone_name>.+)/$', rest_list_views.TimezonesListRestFilter.as_view()),

    #url('^delete_entry/(?P<id>.+)/$', delete_entry.delete_by_id, name='delete_by_id'),


]

