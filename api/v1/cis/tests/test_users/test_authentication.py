from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from mock import patch
from tastypie.authorization import Authorization
from tastypie.test import ResourceTestCase


@patch('api.v1.cis.users.UsersResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def setUp(self):
        super(Test, self).setUp()
        self.obj = get_user_model().objects.create_user('test', 'test')

    def test_get_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'users'})
        self.assertHttpUnauthorized(self.api_client.get(url))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpOK(self.api_client.get(url))

    def test_get_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': self.obj.pk})
        self.assertHttpUnauthorized(self.api_client.get(url))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpOK(self.api_client.get(url))

    def test_post_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'users'})
        self.assertHttpUnauthorized(self.api_client.post(url))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpCreated(self.api_client.post(url))

    def test_put_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'users'})
        self.assertHttpMethodNotAllowed(self.api_client.put(url))

    def test_put_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': self.obj.pk})
        self.assertHttpUnauthorized(self.api_client.put(url))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        # Bad request means we passed auth.
        self.assertHttpBadRequest(self.api_client.put(url))

    def test_patch_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'users'})
        self.assertHttpMethodNotAllowed(self.api_client.patch(url, data=[]))

    def test_patch_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': self.obj.pk})
        data = dict(sex=False)
        self.assertHttpUnauthorized(self.api_client.patch(url, data=data))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpAccepted(self.api_client.patch(url, data=data))

    def test_delete_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'users'})
        self.assertHttpUnauthorized(self.api_client.delete(url))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpAccepted(self.api_client.delete(url))

    def test_delete_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': self.obj.pk})
        self.assertHttpUnauthorized(self.api_client.delete(url))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpAccepted(self.api_client.delete(url))
