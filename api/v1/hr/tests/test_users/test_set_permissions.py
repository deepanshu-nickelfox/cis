from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from mock import patch
from model_mommy import mommy
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v1.hr.users.UsersResource._meta.authentication', Authentication())
@patch('api.v1.hr.users.UsersResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def assertDictEqual(self, d1, d2, msg=None):
        import collections
        for k, v1 in d1.iteritems():
            self.assertIn(k, d2, msg)
            v2 = d2[k]
            if(isinstance(v1, collections.Iterable) and
               not isinstance(v1, basestring)):
                self.assertItemsEqual(v1, v2, msg)
            else:
                self.assertEqual(v1, v2, msg)
        return True

    def test_set_permissions(self):
        obj = mommy.make(get_user_model())
        p1, p2 = mommy.make(Permission, _quantity=2)
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': obj.pk})
        p1_detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'permissions', 'pk': p1.pk})
        p2_detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'permissions', 'pk': p2.pk})

        data = {
            'user_permissions': [p1_detail_url, p2_detail_url],
        }
        resp = self.api_client.put(detail_url, data=data)
        self.assertValidJSONResponse(resp)

        obj = get_user_model().objects.get(pk=obj.pk)
        self.assertEqual(set(obj.user_permissions.all()), {p1, p2})

        self.assertDictContainsSubset({
            'user_permissions': [{
                'id': p1.pk,
                'resource_uri': p1_detail_url,
                'name': p1.name,
                'codename': p1.codename,
            }, {
                'id': p2.pk,
                'resource_uri': p2_detail_url,
                'name': p2.name,
                'codename': p2.codename,
            }]
        }, self.deserialize(resp))
