from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from mock import patch
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v1.hr.users.UsersResource._meta.authentication', Authentication())
@patch('api.v1.hr.users.UsersResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def test_post_list(self):
        list_url = reverse('api_dispatch_list', kwargs={'resource_name': 'users'})
        data = {
            'date_of_birth': '2012-01-01',
            'email': 'test',
            'is_active': True,
            'is_superuser': False,
            'first_name': 'Sandy',
            'last_name': 'Green',
            'middle_name': 'Lagertha',
            'sex': False,
        }
        resp = self.api_client.post(list_url, data=data)
        self.assertHttpCreated(resp)
        obj = get_user_model().objects.latest('id')
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': obj.pk})
        self.assertEqual(self.deserialize(resp), {
            'id': obj.pk,
            'resource_uri': detail_url,
            'created': obj.created.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'modified': obj.modified.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'date_of_birth': data['date_of_birth'] + ' 00:00:00',  # todo: ##fixme##
            'email': data['email'],
            'is_active': data['is_active'],
            'is_superuser': data['is_superuser'],
            'last_login': obj.last_login.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'last_name': data['last_name'],
            'first_name': data['first_name'],
            'middle_name': data['middle_name'],
            'sex': data['sex'],
            'user_permissions': [],
        })
