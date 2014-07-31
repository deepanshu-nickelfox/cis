from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase


class GroupTestAuthentication(APITestCase):

    def test_get_list_raise_403_if_not_authenticated(self):
        url = reverse('api-v1:group-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_raise_403_if_not_admin(self):
        url = reverse('api-v1:group-list')
        get_user_model().objects.create_user('test', 'test')
        ret = self.client.login(email='test', password='test')
        self.assertTrue(ret)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list(self):
        url = reverse('api-v1:group-list')
        get_user_model().objects.create_superuser('test', 'test')
        ret = self.client.login(email='test', password='test')
        self.assertTrue(ret)
        self.client.login(email='test', password='test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GroupTestAPI(APITestCase):

    def setUp(self):
        get_user_model().objects.create_superuser('test', 'test')
        ret = self.client.login(email='test', password='test')
        self.assertTrue(ret)
        self.client.login(email='test', password='test')

    def test_get_list(self):

        obj = mommy.make(Group)

        url = reverse('api-v1:group-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        result_obj = response.data[0]
        self.assertDictEqual(result_obj, {
            'id': obj.id,
            'name': obj.name,
            'permissions': [],
        })
