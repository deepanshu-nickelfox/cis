import uuid
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from mock import patch
from model_mommy import mommy
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v1.cis.groups.GroupsResource._meta.authentication', Authentication())
@patch('api.v1.cis.groups.GroupsResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def test_patch_detail(self):
        obj = mommy.make(Group)
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'groups', 'pk': obj.pk})
        data = {
            'name': str(uuid.uuid4())
        }
        resp = self.api_client.patch(detail_url, data=data)
        self.assertHttpAccepted(resp)
        obj = Group.objects.get(pk=obj.pk)
        self.assertEqual(obj.name, data['name'])

        self.assertEqual(self.deserialize(resp), {
            'id': obj.pk,
            'resource_uri': detail_url,
            'name': obj.name,
            'permissions': [],
        })
