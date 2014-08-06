from django.core.urlresolvers import reverse
from mock import patch
from hr.models import Position
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v1.hr.positions.PositionsResource._meta.authentication', Authentication())
@patch('api.v1.hr.positions.PositionsResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def test_post_list(self):
        list_url = reverse('api_dispatch_list', kwargs={'resource_name': 'positions'})
        data = {
            'name': 'Sandy'
        }
        resp = self.api_client.post(list_url, data=data)
        self.assertHttpCreated(resp)
        obj = Position.objects.latest('id')
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'positions', 'pk': obj.pk})
        self.assertEqual(self.deserialize(resp), {
            'id': obj.pk,
            'resource_uri': detail_url,
            'name': data['name'],
            'department': None,
        })
