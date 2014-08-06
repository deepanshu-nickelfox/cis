from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from model_mommy import mommy
from hr.models import Position
from tastypie.test import ResourceTestCase


class Test(ResourceTestCase):

    def setUp(self):
        super(Test, self).setUp()
        self.user = get_user_model().objects.create_user('test', 'test')
        self.obj = mommy.make(Position)

    def test_get_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'positions'})
        self.assertHttpUnauthorized(self.api_client.get(url))
        self.user.user_permissions.add(Permission.objects.get(codename='read_position'))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpOK(self.api_client.get(url))

    def test_get_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'positions', 'pk': self.obj.pk})
        self.assertHttpUnauthorized(self.api_client.get(url))
        self.user.user_permissions.add(Permission.objects.get(codename='read_position'))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpOK(self.api_client.get(url))

    def test_post_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'positions'})
        self.assertHttpUnauthorized(self.api_client.post(url))
        self.user.user_permissions.add(Permission.objects.get(codename='add_position'))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpCreated(self.api_client.post(url))

    def test_put_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'positions', 'pk': self.obj.pk})
        self.assertHttpUnauthorized(self.api_client.put(url))
        self.user.user_permissions.add(Permission.objects.get(codename='change_position'))
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        # Bad request means we passed auth.
        self.assertHttpBadRequest(self.api_client.put(url))

    def test_patch_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'positions', 'pk': self.obj.pk})
        data = dict(sex=False)
        self.assertHttpUnauthorized(self.api_client.patch(url, data=data))
        self.user.user_permissions.add(
            Permission.objects.get(codename='change_position'),
            Permission.objects.get(codename='read_position'),
        )
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpAccepted(self.api_client.patch(url, data=data))

    def test_delete_list(self):
        url = reverse('api_dispatch_list', kwargs={'resource_name': 'positions'})
        self.assertHttpUnauthorized(self.api_client.delete(url))
        self.user.user_permissions.add(
            Permission.objects.get(codename='delete_position'),
            Permission.objects.get(codename='read_position'),
        )
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpAccepted(self.api_client.delete(url))

    def test_delete_detail(self):
        url = reverse('api_dispatch_detail', kwargs={'resource_name': 'positions', 'pk': self.obj.pk})
        self.assertHttpUnauthorized(self.api_client.delete(url))
        self.user.user_permissions.add(
            Permission.objects.get(codename='delete_position'),
            Permission.objects.get(codename='read_position'),
        )
        self.assertTrue(self.api_client.client.login(email='test', password='test'))
        self.assertHttpAccepted(self.api_client.delete(url))
