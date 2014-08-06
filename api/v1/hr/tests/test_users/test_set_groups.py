from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from mock import patch
from model_mommy import mommy
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v1.hr.users.UsersResource._meta.authentication', Authentication())
@patch('api.v1.hr.users.UsersResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def test_set_groups(self):
        obj = mommy.make(get_user_model())
        group = mommy.make(Group)
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': obj.pk})
        group_detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'groups', 'pk': group.pk})

        data = {
            'groups': [group_detail_url],
        }
        resp = self.api_client.put(detail_url, data=data)
        self.assertValidJSONResponse(resp)

        obj = get_user_model().objects.get(pk=obj.pk)
        self.assertEqual(set(obj.groups.all()), {group})

        self.assertDictContainsSubset({
            'groups': [{
                'id': group.pk,
                'resource_uri': group_detail_url,
                'name': group.name,
                'permissions': [],
            }]
        }, self.deserialize(resp))
