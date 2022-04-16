from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token


class RegistrationTests(APITestCase):

    def test_registration(self):
        data = {
            'username': 'TestUser',
            'password': 'testpass1234'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CountryTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='TestUser', password='testpass1234')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.login(user=self.user)

    def test_country_list(self):
        print(User.objects.all())
        response = self.client.get('/api/country/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_authentication(self):
        self.assertEqual(self.user.is_authenticated, True)

    def test_create_country_authenticated(self):
        data = {
            'name': 'TestCountry',
            'iso': 'TC',
            'flag': 'test.jpg',
        }
        response = self.client.post('/api/country/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)