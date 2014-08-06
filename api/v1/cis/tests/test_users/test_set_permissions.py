from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from mock import patch
from model_mommy import mommy
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v1.cis.users.UsersResource._meta.authentication', Authentication())
@patch('api.v1.cis.users.UsersResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def test_set_permissions(self):
        obj = mommy.make(get_user_model())
        perm = mommy.make(Permission)
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': obj.pk})
        perm_detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'permissions', 'pk': perm.pk})

        data = {
            'user_permissions': [perm_detail_url],
        }
        resp = self.api_client.put(detail_url, data=data)
        self.assertValidJSONResponse(resp)

        obj = get_user_model().objects.get(pk=obj.pk)
        self.assertEqual(set(obj.user_permissions.all()), {perm})

        self.assertDictContainsSubset({
            'user_permissions': [{
                'id': perm.pk,
                'resource_uri': perm_detail_url,
                'name': perm.name,
                'codename': perm.codename,
            }]
        }, self.deserialize(resp))
