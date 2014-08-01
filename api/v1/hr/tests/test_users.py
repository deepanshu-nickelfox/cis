from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cis.models import User


class UserTestAuthentication(APITestCase):

    def test_get_list(self):
        url = reverse('api-v1:user-list')
        get_user_model().objects.create_superuser('test', 'test')
        ret = self.client.login(email='test', password='test')
        self.assertTrue(ret)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_raise_403_if_not_authenticated(self):
        url = reverse('api-v1:user-list')
        response = self.client.post(url, data={
            'email': 'test@example.com',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_raise_403_if_not_is_admin(self):
        url = reverse('api-v1:user-list')
        get_user_model().objects.create_user('test', 'test')
        self.assertTrue(self.client.login(email='test', password='test'))
        response = self.client.post(url, data={
            'email': 'test@example.com',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user(self):
        url = reverse('api-v1:user-list')
        get_user_model().objects.create_superuser('test', 'test')
        self.assertTrue(self.client.login(email='test', password='test'))

        data = {
            'email': 'test@example.com',
            'first_name': 'Simone',
            'last_name': 'Simons',
            'middle_name': None,
            'sex': User.FEMALE,
            'password': '12345',
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data.pop('password')
        self.assertDictContainsSubset(data, response.data)

    def test_create_user_and_login(self):
        url = reverse('api-v1:user-list')
        get_user_model().objects.create_superuser('test', 'test')
        self.assertTrue(self.client.login(email='test', password='test'))

        data = {
            'email': 'test@example.com',
            'password': '123',
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data.pop('password')
        self.assertDictContainsSubset(data, response.data)

        self.client.logout()
        self.assertTrue(self.client.login(email='test@example.com', password='123'))


class UserTestAPI(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser('test', 'test')
        ret = self.client.login(email='test', password='test')
        self.assertTrue(ret)

    def test_get_list(self):
        url = reverse('api-v1:user-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_detail(self):
        url = reverse('api-v1:user-detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, {
            'id': self.user.id,
            'email': self.user.email,
            'user_permissions': [],
            'groups': [],
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'middle_name': self.user.middle_name,
            'sex': self.user.sex,
            'date_of_birth': self.user.date_of_birth,
            'is_superuser': self.user.is_superuser,
        })
