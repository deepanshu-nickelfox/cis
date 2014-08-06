from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from model_mommy import mommy
from tastypie.test import ResourceTestCase


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
