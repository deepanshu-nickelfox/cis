from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import APITestCase


class UserTestGet(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser('test', 'test')
        self.assertTrue(self.client.login(email='test', password='test'))

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


class UserTestPost(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser('test', 'test')
        self.assertTrue(self.client.login(email='test', password='test'))

    def test_create_user_and_login(self):
        url = reverse('api-v1:user-list')
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


class UserTestPatch(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser('test', 'test')
        self.assertTrue(self.client.login(email='test', password='test'))

    def test_create_user_and_patch_it(self):
        user = mommy.make(get_user_model(), sex=False)
        url = reverse('api-v1:user-detail', kwargs={'pk': user.pk})
        data = {
            'sex': True
        }
        response = self.client.patch(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(data, response.data)


class UserTestPut(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser('test', 'test')
        self.assertTrue(self.client.login(email='test', password='test'))

    def test_create_user_and_update_it(self):
        user = mommy.make(get_user_model(), sex=False)
        url = reverse('api-v1:user-detail', kwargs={'pk': user.pk})
        data = {
            'email': user.email,
            'sex': True,
        }
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(data, response.data)


class UserTestAuthentication(APITestCase):

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
