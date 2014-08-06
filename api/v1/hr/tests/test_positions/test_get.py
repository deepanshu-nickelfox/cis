from django.core.urlresolvers import reverse
from mock import patch
from model_mommy import mommy
from hr.models import Position
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v1.hr.positions.PositionsResource._meta.authentication', Authentication())
@patch('api.v1.hr.positions.PositionsResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def setUp(self):
        super(Test, self).setUp()
        self.obj = mommy.make(Position)

    def test_get_list(self):
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'positions', 'pk': self.obj.pk})
        list_url = reverse('api_dispatch_list', kwargs={'resource_name': 'positions'})
        resp = self.api_client.get(list_url)
        self.assertValidJSONResponse(resp)

        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        # Here, we're checking an entire structure for the expected data.
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            'id': self.obj.pk,
            'resource_uri': detail_url,
            'name': self.obj.name,
            'department': self.obj.department,
        })

    def test_get_detail(self):
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'positions', 'pk': self.obj.pk})
        resp = self.api_client.get(detail_url)
        self.assertValidJSONResponse(resp)

        # Here, we're checking an entire structure for the expected data.
        self.assertEqual(self.deserialize(resp), {
            'id': self.obj.pk,
            'resource_uri': detail_url,
            'name': self.obj.name,
            'department': self.obj.department,
        })
