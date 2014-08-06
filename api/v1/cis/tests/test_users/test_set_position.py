from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import override_settings
from mock import patch
from model_mommy import mommy
from hr.models import Position
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v1.cis.users.UsersResource._meta.authentication', Authentication())
@patch('api.v1.cis.users.UsersResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    @override_settings(FEATURE_REQUIRE_READ_PRIVILEGES=False)
    def test_set_position(self):
        obj = mommy.make(get_user_model())
        position = mommy.make(Position)
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': obj.pk})
        position_detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'positions', 'pk': position.pk})

        data = {
            'position': position_detail_url,
        }
        resp = self.api_client.put(detail_url, data=data)
        self.assertValidJSONResponse(resp)

        obj = get_user_model().objects.get(pk=obj.pk)
        self.assertEqual(obj.position, position)

        self.assertDictContainsSubset({
            'position': {
                'id': position.pk,
                'resource_uri': position_detail_url,
                'name': position.name,
                'department': None,
            }
        }, self.deserialize(resp))
