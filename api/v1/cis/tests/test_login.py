from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestLogin(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser('test', 'test')

    def test_login(self):
        url = reverse('api-v1-login')
        response = self.client.post(url, data={'email': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        url = reverse('api-v1-login')
        response = self.client.post(url, data={'email': 'invalidemail', 'password': 'invalid password'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
