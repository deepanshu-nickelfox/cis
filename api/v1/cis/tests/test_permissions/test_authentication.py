from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from mock import patch
from model_mommy import mommy
from tastypie.authorization import Authorization
from tastypie.test import ResourceTestCase


@patch('api.v1.cis.permissions.PermissionsResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def setUp(self):
        super(Test, self).setUp()
        get_user_model().objects.create_user('test', 'test')
        self.obj = mommy.make(Permission)

    def test_get_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'permissions'})
        self.assertHttpUnauthorized(self.api_client.get(url))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpOK(self.api_client.get(url))

    def test_get_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'permissions', 'pk': self.obj.pk})
        self.assertHttpUnauthorized(self.api_client.get(url))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpOK(self.api_client.get(url))

    def test_post_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'permissions'})
        self.assertHttpMethodNotAllowed(self.api_client.post(url))

    def test_put_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'permissions'})
        self.assertHttpMethodNotAllowed(self.api_client.put(url))

    def test_put_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'permissions', 'pk': self.obj.pk})
        self.assertHttpMethodNotAllowed(self.api_client.put(url))

    def test_patch_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'permissions'})
        self.assertHttpMethodNotAllowed(self.api_client.patch(url, data=[]))

    def test_patch_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'permissions', 'pk': self.obj.pk})
        self.assertHttpMethodNotAllowed(self.api_client.patch(url, data=[]))

    def test_delete_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'permissions'})
        self.assertHttpMethodNotAllowed(self.api_client.delete(url))

    def test_delete_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'permissions', 'pk': self.obj.pk})
        self.assertHttpMethodNotAllowed(self.api_client.delete(url))
