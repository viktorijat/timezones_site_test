from django.test import TransactionTestCase
from django.contrib.auth.models import User
from zonesapp.models import UserEntry, Timezones
from zonesapp.views import register, submit_entry
from django.http import HttpRequest
import requests
#python manage.py test zonesapp


class LoginTestCase(TransactionTestCase):

    def test_index(self):
        resp = self.client.get('/log_in_form_event/')
        self.assertEqual(resp.status_code, 405)


class RegisterTest(TransactionTestCase):

    def test_index(self):
        resp = self.client.get('/register_form_event/')
        self.assertEqual(resp.status_code, 405)


class CreateEntry(TransactionTestCase):

    def setUp(self):

        # Every test needs access to the request factory.
        self.user = User.objects.create_user(username='new_user_test',
                                             email='test@test.com',
                                             password='test_password',)

    def create_user_test(self):

        client = requests.session()
        client.get('/register_form_event/')
        csrftoken = client.cookies['csrf']

        request_reqister = HttpRequest
        request_reqister.method = "PUT"
        request_reqister.username = "new_test_user2"
        request_reqister.email = "test2@test.com"
        request_reqister.password = "test_password2"
        request_reqister.csrfmiddlewaretoken = csrftoken

        response = register.register_form_event(request_reqister)
        self.assertEqual(response.status_code, 200)

    def create_entry_test(self):

        #request_entry = self.client.get('/profile/submit_entry/')
        request_entry = HttpRequest
        request_entry.method = "POST"
        request_entry.entry_name = "test_entry"
        request_entry.city_name = "test_city"
        request_entry.gmt_offset = "09:00"
        request_entry.user = self.user
        response = submit_entry.submit_entry(request_entry)
        self.assertEqual(response.status_code, 200)


