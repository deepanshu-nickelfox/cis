from django.contrib.auth.models import Permission, Group
from django.core.urlresolvers import reverse
from mock import patch
from model_mommy import mommy
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v1.cis.groups.GroupsResource._meta.authentication', Authentication())
@patch('api.v1.cis.groups.GroupsResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def test_set_permissions(self):
        obj = mommy.make(Group)
        perm = mommy.make(Permission)
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'groups', 'pk': obj.pk})
        perm_detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'permissions', 'pk': perm.pk})

        data = {
            'permissions': [perm_detail_url],
        }
        resp = self.api_client.put(detail_url, data=data)
        self.assertValidJSONResponse(resp)

        obj = Group.objects.get(pk=obj.pk)
        self.assertEqual(set(obj.permissions.all()), {perm})

        self.assertDictContainsSubset({
            'permissions': [{
                'id': perm.pk,
                'resource_uri': perm_detail_url,
                'name': perm.name,
                'codename': perm.codename,
            }]
        }, self.deserialize(resp))
