from django.test import TransactionTestCase
from django.contrib.auth.models import User
from zonesapp.models import UserEntry, Timezones
from zonesapp.views import register, submit_entry
from django.http import HttpRequest
import requests
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import authenticate, login
from zonesapp.views.list_view import *
from zonesapp.views.submit_entry import *
from zonesapp.views.logout import *
from zonesapp.views.log_in import *
from zonesapp.views.delete_entry import *
from zonesapp.views.edit_entry import *
from timezones_site import settings, test_settings
import os
from django.test import Client
from django.http import QueryDict



###########################################################
#export PYTHONPATH=$PYTHONPATH:/home/krste/timezones_site
#export DJANGO_SETTINGS_MODULE=timezones_site.test_settings
#py.test zonesapp/tests.py
###########################################################



@pytest.mark.django_db
class TestViews:

    def test_home(self, client):
        resp = client.post('/')
        print resp
        assert resp.status_code == 200

    def test_login(self, client):

        user = User.objects.create_user(username='test_user', email='test@test.com', password='test_password')
        user.save()
        resp = client.post('/log_in_form_event/', 'name=test_user&password=test_password', 'application/x-www-form-urlencoded', HTTP_AUTHORIZATION="Basic " + base64.b64encode("test_user:test_password"))
        assert resp.status_code == 200

    def test_login_wrong_method(self, client):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user', email='test@test.com', password='test_password')
        resp = client.put('/log_in_form_event/', 'name=test_user&password=test_password', 'application/x-www-form-urlencoded')
        assert resp.status_code == 405

    def test_login_wrong(self, client):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user', email='test@test.com', password='test_password')
        resp = client.post('/log_in_form_event/', 'name=test_user2&password=test_password', 'application/x-www-form-urlencoded')
        assert resp.status_code == 401

    def test_register(self, client):
        resp = client.post('/register_form_event/', 'name=tname&email=tname@asd.com&password=tname&password1=tname', 'application/x-www-form-urlencoded')
        assert resp.status_code == 201


    def test_register_conflict(self, client):
        user = User.objects.create_user(username='tname', email='tname@asd.com', password='tname')
        resp = client.post('/register_form_event/', 'name=tname&email=tname@asd.com&password=tname&password1=tname', 'application/x-www-form-urlencoded')
        assert resp.status_code == 409

    def test_register_wrong(self, client):
        resp = client.post('/register_form_event/', 'name=tname&email=tname@asd.com&password=tname2&password1=tname', 'application/x-www-form-urlencoded')
        assert resp.status_code == 400

    def test_register_wrong_method(self, client):
        resp = client.put('/register_form_event/', 'name=tname&email=tname@asd.com&password=tname&password1=tname', 'application/x-www-form-urlencoded')
        assert resp.status_code == 405


    def test_entry_list_no_entries(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user', email='test@test.com', password='test_password')
        request = factory.get('/entry_list/')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user:test_password")
        request.user = user
        response = entry_list(request)
        assert response.status_code == 404

    def test_entry_list_one_entry(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user2', email='test2@test.com', password='test_password2')
        entry = UserEntry(entry_name='test_entry', city_name='test_city',user=user,gmt_offset_display="02:00")
        entry.save()
        request = factory.get('/entry_list/')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user2:test_password2")
        request.user = user
        response = entry_list(request)
        assert response.status_code == 200

    def test_entry_list_wrong_method(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user2', email='test2@test.com', password='test_password2')
        entry = UserEntry(entry_name='test_entry', city_name='test_city',user=user,gmt_offset_display="02:00")
        entry.save()
        request = factory.put('/entry_list/')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user2:test_password2")
        request.user = user
        response = entry_list(request)
        assert response.status_code == 405

    def test_entry_list_no_user(self, client):

        user = User.objects.create_user(username='test_user2', email='test2@test.com', password='test_password2')
        entry = UserEntry(entry_name='test_entry', city_name='test_city',user=user,gmt_offset_display="02:00")
        entry.save()
        resp = client.post('/entry_list/')
        assert resp.status_code == 401


    def test_get_current_time(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        entry = UserEntry(entry_name='test_entry2', city_name='test_city2', user=user, gmt_offset_display="02:00")
        entry.save()
        request = factory.get('/get_current_time/1/')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = get_current_time(request, 1)
        assert response.status_code == 200

    def test_get_current_time_wrong_method(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        entry = UserEntry(entry_name='test_entry2', city_name='test_city2', user=user, gmt_offset_display="02:00")
        entry.save()
        request = factory.put('/get_current_time/1/')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = get_current_time(request, 1)
        assert response.status_code == 405

    def test_get_current_time_no_entries(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        entry = UserEntry(entry_name='test_entry2', city_name='test_city2', user=user, gmt_offset_display="02:00")
        entry.save()
        request = factory.get('/get_current_time/2/')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = get_current_time(request, 2)
        assert response.status_code == 404

    def test_get_current_time_no_user(self, client):

        user = User.objects.create_user(username='test_user2', email='test2@test.com', password='test_password2')
        entry = UserEntry(entry_name='test_entry', city_name='test_city',user=user,gmt_offset_display="02:00")
        entry.save()
        resp = client.post('/get_current_time/2/')
        assert resp.status_code == 401


    def test_submit_entry(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        request = factory.put('/submit_entry/', 'entry_name=tname&city_name=London&gmt_offset=02:00')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = submit_entry(request)
        assert response.status_code == 201

    def test_submit_entry_no_user(self, client):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user2', email='test2@test.com', password='test_password2')
        entry = UserEntry(entry_name='test_entry', city_name='test_city',user=user,gmt_offset_display="02:00")
        entry.save()
        resp = client.put('/submit_entry/', 'entry_name=tname&city_name=London&gmt_offset=02:00')
        assert resp.status_code == 401


    def test_submit_entry_wrong_method(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        request = factory.post('/submit_entry/', 'entry_name=tname&city_name=London&gmt_offset=02:00', 'application/x-www-form-urlencoded')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = submit_entry(request)
        assert response.status_code == 405


    def test_submit_entry_exists(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        entry = UserEntry(entry_name='tname', city_name='London',user=user,gmt_offset_display="02:00")
        entry.save()
        request = factory.put('/submit_entry/', 'entry_name=tname&city_name=London&gmt_offset=02:00')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = submit_entry(request)
        assert response.status_code == 409


    def test_check_city(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        authenticate(username='test_user3', password='test_password3')
        request = factory.get('/check_city/', {'query': 'London'})
        request.user = user
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        response = check_city(request)
        assert response.status_code == 200

    def test_check_city_wrong_method(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        request = factory.put('/check_city/', {'city_name': 'London'})
        request.user = user
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        response = check_city(request)
        assert response.status_code == 405


    def test_check_city_no_user(self, client):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user2', email='test2@test.com', password='test_password2')
        resp = client.post('/check_city/', 'city_name=London', 'application/x-www-form-urlencoded')
        assert resp.status_code == 401


    def test_logout(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        request = factory.post('/logout_event/')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.user = user
        response = logout_event(request)
        assert response.status_code == 200



    def test_logout_no_user(self, client):

        resp = client.post('/logout_event/')
        assert resp.status_code == 401


    def test_logout_wrong_user(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        request = factory.put('/logout_event/')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        request.user = user
        response = logout_event(request)
        assert response.status_code == 405



    def test_delete_entry(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        entry = UserEntry(entry_name='test_entry2', city_name='test_city2', user=user, gmt_offset_display="02:00")
        entry.save()
        request = factory.delete('/delete_by_id/1/')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = delete_by_id(request, 1)
        assert response.status_code == 200

    def test_delete_entry_doesnt_exist(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        request = factory.delete('/delete_by_id/1/')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = delete_by_id(request, 1)
        assert response.status_code == 404


    def test_delete_entry_no_user(self, client):

        resp = client.post('/delete_by_id/1/')
        assert resp.status_code == 401


    def test_delete_entry_wrong_method(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        entry = UserEntry(entry_name='test_entry2', city_name='test_city2', user=user, gmt_offset_display="02:00")
        entry.save()
        request = factory.put('/delete_by_id/1/')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = delete_by_id(request, 1)
        assert response.status_code == 405



    def test_edit_entry(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        entry = UserEntry(entry_name='test_entry2', city_name='test_city2', user=user, gmt_offset_display="02:00")
        entry.save()
        request = factory.put('/edit_by_id/1/', 'entry_name=test_entry3&city_name=test_city3&offset=03:00')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = edit_by_id(request, 1)
        assert response.status_code == 200


    def test_edit_entry_validation_error(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        entry = UserEntry(entry_name='test_entry2', city_name='test_city2', user=user, gmt_offset_display="02:00")
        entry.save()
        request = factory.put('/edit_by_id/1/', 'entry_name=test_entry3&city_name=test_city3&offset=b')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = edit_by_id(request, 1)
        assert response.status_code == 400


    def test_edit_entry_doesnt_exist(self):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        entry = UserEntry(entry_name='test_entry2', city_name='test_city2', user=user, gmt_offset_display="02:00")
        entry.save()
        request = factory.put('/edit_by_id/2/', 'entry_name=test_entry3&city_name=test_city3&offset=03:00')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = edit_by_id(request, 2)
        assert response.status_code == 404


    def test_edit_entry_no_user(self, client):

        resp = client.post('/edit_by_id/1/')
        assert resp.status_code == 401


    def test_edit_entry_wrong_method(self, client):

        factory = RequestFactory()
        user = User.objects.create_user(username='test_user3', email='test3@test.com', password='test_password3')
        entry = UserEntry(entry_name='test_entry2', city_name='test_city2', user=user, gmt_offset_display="02:00")
        entry.save()
        request = factory.post('/edit_by_id/1/', 'entry_name=test_entry3&city_name=test_city3&offset=03:00', 'application/x-www-form-urlencoded')
        request.META['HTTP_AUTHORIZATION'] = "Basic " + base64.b64encode("test_user3:test_password3")
        request.user = user
        response = edit_by_id(request, 1)
        assert response.status_code == 405
