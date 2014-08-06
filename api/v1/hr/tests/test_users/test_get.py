from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from mock import patch
from model_mommy import mommy
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v1.hr.users.UsersResource._meta.authentication', Authentication())
@patch('api.v1.hr.users.UsersResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def setUp(self):
        super(Test, self).setUp()
        self.obj = mommy.make(get_user_model())

    def test_get_list(self):
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': self.obj.pk})
        list_url = reverse('api_dispatch_list', kwargs={'resource_name': 'users'})
        resp = self.api_client.get(list_url)
        self.assertValidJSONResponse(resp)

        self.assertEqual(len(self.deserialize(resp)['objects']), 1)
        # Here, we're checking an entire structure for the expected data.
        self.assertEqual(self.deserialize(resp)['objects'][0], {
            'id': self.obj.pk,
            'resource_uri': detail_url,
            'created': self.obj.created.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'modified': self.obj.modified.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'date_of_birth': self.obj.date_of_birth,
            'email': self.obj.email,
            'is_active': self.obj.is_active,
            'is_superuser': self.obj.is_superuser,
            'last_login': self.obj.last_login.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'last_name': self.obj.last_name,
            'first_name': self.obj.first_name,
            'middle_name': self.obj.middle_name,
            'sex': self.obj.sex,
        })

    def test_get_detail(self):
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': self.obj.pk})
        resp = self.api_client.get(detail_url)
        self.assertValidJSONResponse(resp)

        # Here, we're checking an entire structure for the expected data.
        self.assertEqual(self.deserialize(resp), {
            'id': self.obj.pk,
            'resource_uri': detail_url,
            'created': self.obj.created.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'modified': self.obj.modified.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'date_of_birth': self.obj.date_of_birth,
            'email': self.obj.email,
            'is_active': self.obj.is_active,
            'is_superuser': self.obj.is_superuser,
            'last_login': self.obj.last_login.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'last_name': self.obj.last_name,
            'first_name': self.obj.first_name,
            'middle_name': self.obj.middle_name,
            'sex': self.obj.sex,
        })
