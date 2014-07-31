from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserTestAuthentication(APITestCase):

    def test_get_list_raise_403_if_not_authenticated(self):
        url = reverse('api-v1:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_raise_403_if_not_admin(self):
        url = reverse('api-v1:user-list')
        get_user_model().objects.create_user('test', 'test')
        ret = self.client.login(email='test', password='test')
        self.assertTrue(ret)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list(self):
        url = reverse('api-v1:user-list')
        get_user_model().objects.create_superuser('test', 'test')
        ret = self.client.login(email='test', password='test')
        self.assertTrue(ret)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
