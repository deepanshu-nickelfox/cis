from django.contrib.auth.models import Group
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

    def test_set_department(self):
        obj = mommy.make(Position)
        group = mommy.make(Group)
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'positions', 'pk': obj.pk})
        group_detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'groups', 'pk': group.pk})

        data = {
            'department': group_detail_url,
        }
        resp = self.api_client.put(detail_url, data=data)
        self.assertValidJSONResponse(resp)

        obj = Position.objects.get(pk=obj.pk)
        self.assertEqual(obj.department, group)

        self.assertDictContainsSubset({
            'department': {
                'id': group.pk,
                'resource_uri': group_detail_url,
                'name': group.name,
                'permissions': [],
            }
        }, self.deserialize(resp))
