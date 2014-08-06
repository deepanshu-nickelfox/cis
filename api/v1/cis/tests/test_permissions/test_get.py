from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from mock import patch
from model_mommy import mommy
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v1.cis.permissions.PermissionsResource._meta.authentication', Authentication())
@patch('api.v1.cis.permissions.PermissionsResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def setUp(self):
        super(Test, self).setUp()
        self.obj = mommy.make(Permission)

    def test_get_list(self):
        list_url = reverse('api_dispatch_list', kwargs={'resource_name': 'permissions'})
        resp = self.api_client.get(list_url)
        self.assertValidJSONResponse(resp)

        self.assertEqual(
            len(self.deserialize(resp)['objects']),
            Permission.objects.all().count())

        self.assertKeys(
            self.deserialize(resp)['objects'][0],
            ['id', 'resource_uri', 'codename', 'name'])

    def test_get_detail(self):
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'permissions', 'pk': self.obj.pk})
        resp = self.api_client.get(detail_url)
        self.assertValidJSONResponse(resp)

        # Here, we're checking an entire structure for the expected data.
        self.assertEqual(self.deserialize(resp), {
            'id': self.obj.pk,
            'resource_uri': detail_url,
            'codename': self.obj.codename,
            'name': self.obj.name,
        })
