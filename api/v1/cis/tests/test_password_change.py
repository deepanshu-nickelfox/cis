from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestPasswordChange(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_superuser('test', 'test')
        ret = self.client.login(email='test', password='test')
        self.assertTrue(ret)

    def test_change_password_invalid_current_password(self):
        url = reverse('api-v1:user-set-password', kwargs={'pk': self.user.pk})
        response = self.client.post(url, data={
            'current_password': 'invalidpass',
            'password1': 'newpass',
            'password2': 'newpass',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_mismatched_confirmation(self):
        url = reverse('api-v1:user-set-password', kwargs={'pk': self.user.pk})
        response = self.client.post(url, data={
            'current_password': 'test',
            'password1': 'newpass',
            'password2': 'newpass-mismatched',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        url = reverse('api-v1:user-set-password', kwargs={'pk': self.user.pk})
        response = self.client.post(url, data={
            'current_password': 'test',
            'password1': 'newpass',
            'password2': 'newpass',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        ret = self.client.login(email='test', password='newpass')
        self.assertTrue(ret)
