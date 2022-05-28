from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from cities.models import City, Country
from cities.utilities import temporary_image


class RegistrationTests(APITestCase):

    def test_registration(self):
        self.assertEqual(len(User.objects.all()), 0)
        data = {
            'username': 'TestUser',
            'password': 'testpass1234'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username='TestUser')
        self.assertEqual(user.username, 'TestUser')


class CountryCreateTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='TestUser', password='testpass1234')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.login(user=self.user)
        self.data = {
            "name": "TestCountry",
            "iso": "TC",
            "flag": temporary_image()
        }

    def test_authentication(self):
        self.assertEqual(self.user.is_authenticated, True)

    def test_create_country_authenticated(self):

        response = self.client.post('/api/country/create/', self.data)
        country_id = response.data.get('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(f'/api/country/{country_id}/')
        self.assertEqual(response.data.get('name'), "TestCountry")

    def test_create_country_un_authenticated(self):
        self.client.logout()
        response = self.client.post('/api/country/create/', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CountryUpdateDestroyTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='TestUser', password='testpass1234')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.login(user=self.user)
        data = {
            "name": "TestCountry",
            "iso": "TC",
            "flag": temporary_image()
        }
        response = self.client.post('/api/country/create/', data)
        self.country_id = response.data.get('id')

    def test_country_list(self):
        response = self.client.get('/api/country/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_country(self):
        response = self.client.get(f'/api/country/{self.country_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data.get('name'), "TestCountry")
        self.assertContains(response, 'id')
        self.assertContains(response, 'iso')
        self.assertContains(response, 'population')

    def test_country_update_authenticated(self):
        changed_data = {
            "name": "New Country Name",
            "iso": "СC",
            "flag": temporary_image()
        }
        response = self.client.put(f'/api/country/update/{self.country_id}/', changed_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), "New Country Name")
        self.assertEqual(response.data.get('iso'), "СC")
        self.assertEqual(response.data.get('population'), 0)

        response = self.client.patch(f'/api/country/update/{self.country_id}/', {'population': 1000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('population'), 1000)

    def test_country_update_un_authenticated(self):
        self.client.logout()
        changed_data = {
            "name": "New Country Name",
            "iso": "СC",
            "flag": temporary_image()
        }
        response = self.client.put(f'/api/country/update/{self.country_id}/', changed_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.patch(f'/api/country/update/{self.country_id}/', {'population': 1000})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_country_delete_un_authenticated(self):
        self.client.logout()
        response = self.client.delete(f'/api/country/delete/{self.country_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_country_delete_authenticated_as_not_admin(self):
        self.assertEqual(self.user.is_staff, False)
        response = self.client.delete(f'/api/country/delete/{self.country_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_country_delete_authenticated_as_admin(self):
        response = self.client.get(f'/api/country/{self.country_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.country_id)
        self.assertEqual(response.data.get('name'), "TestCountry")

        self.user.is_staff = True
        self.user.save()
        self.assertEqual(self.user.is_staff, True)
        response = self.client.delete(f'/api/country/delete/{self.country_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/api/country/{self.country_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CityCreateTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='TestUser', password='testpass1234')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.login(user=self.user)
        country_data = {
            "name": "SomeCountry",
            "iso": "SC",
            "flag": temporary_image()
        }
        response = self.client.post('/api/country/create/', country_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.country_id = response.data.get('id')
        self.city_data = {
            "name": "TestCity",
            "population": 1500,
            "slug": 'testcity',
            "flag": temporary_image(),
            "has_mcdonalds": True
        }

    def test_create_city_authenticated(self):
        response = self.client.post(f'/api/country/{self.country_id}/city/create/', self.city_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        city_id = response.data.get('id')
        response = self.client.get(f'/api/city/{city_id}/')
        self.assertEqual(response.data.get('name'), "TestCity")

    def test_create_country_un_authenticated(self):
        self.client.logout()
        response = self.client.post(f'/api/country/{self.country_id}/city/create/', self.city_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CityUpdateDestroyTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='TestUser', password='testpass1234')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.login(user=self.user)

        country_data = {
            "name": "SomeCountry",
            "iso": "SC",
            "flag": temporary_image()
        }
        response = self.client.post('/api/country/create/', country_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        country_id = response.data.get('id')

        city_data = {
            "name": "TestCity",
            "population": 1500,
            "slug": 'testcity',
            "flag": temporary_image(),
            "has_mcdonalds": True
        }
        response = self.client.post(f'/api/country/{country_id}/city/create/', city_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.city_id = response.data.get('id')

    def test_city_list(self):
        response = self.client.get('/api/city/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_city(self):
        response = self.client.get(f'/api/city/{self.city_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.data.get('id'), self.city_id)
        self.assertEqual(response.data.get('name'), "TestCity")
        self.assertEqual(response.data.get('population'), 1500)
        self.assertContains(response, 'slug')
        self.assertContains(response, 'flag')
        self.assertContains(response, 'has_mcdonalds')

    def test_city_update_authenticated(self):
        changed_data = {
            "name": "Some New Name",
            "population": 1500,
            "slug": 'new_slug',
            "flag": temporary_image(),
            "has_mcdonalds": True
        }
        response = self.client.put(f'/api/city/{self.city_id}/update/', changed_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), "Some New Name")
        self.assertEqual(response.data.get('slug'), "new_slug")
        self.assertEqual(response.data.get('population'), 1500)

        response = self.client.patch(f'/api/city/{self.city_id}/update/', {'population': 2500})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('population'), 2500)

    def test_city_update_un_authenticated(self):
        self.client.logout()
        changed_data = {
            "name": "Some New Name",
            "population": 1500,
            "slug": 'new_slug',
            "flag": temporary_image(),
            "has_mcdonalds": True
        }
        response = self.client.put(f'/api/city/{self.city_id}/update/', changed_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.patch(f'/api/city/{self.city_id}/update/', {'has_mcdonalds': False})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_city_delete_un_authenticated(self):
        self.client.logout()
        response = self.client.delete(f'/api/city/{self.city_id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_city_delete_authenticated_as_not_admin(self):
        self.assertEqual(self.user.is_staff, False)
        response = self.client.delete(f'/api/city/{self.city_id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_city_delete_authenticated_as_admin(self):
        response = self.client.get(f'/api/city/{self.city_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), "TestCity")
        self.assertEqual(response.data.get('slug'), "testcity")
        self.assertEqual(response.data.get('id'), self.city_id)

        self.user.is_staff = True
        self.user.save()
        self.assertEqual(self.user.is_staff, True)
        response = self.client.delete(f'/api/city/{self.city_id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/api/country/{self.city_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)