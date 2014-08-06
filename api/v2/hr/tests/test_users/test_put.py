import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from mock import patch
from model_mommy import mommy
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.test import ResourceTestCase


@patch('api.v2.hr.users.UsersResource._meta.authentication', Authentication())
@patch('api.v2.hr.users.UsersResource._meta.authorization', Authorization())
class Test(ResourceTestCase):

    def test_put_detail(self):
        obj = mommy.make(get_user_model())
        detail_url = reverse('api_dispatch_detail', kwargs={'resource_name': 'users', 'pk': obj.pk})
        data = {
            'first_name': str(uuid.uuid4())
        }
        resp = self.api_client.put(detail_url, data=data)
        self.assertValidJSONResponse(resp)

        obj = get_user_model().objects.get(pk=obj.pk)
        self.assertEqual(obj.first_name, data['first_name'])

        self.assertEqual(self.deserialize(resp), {
            'id': obj.pk,
            'resource_uri': detail_url,
            'created': obj.created.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'modified': obj.modified.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'date_of_birth': obj.date_of_birth,
            'email': obj.email,
            'is_active': obj.is_active,
            'is_superuser': obj.is_superuser,
            'last_login': obj.last_login.strftime(settings.TASTYPIE_DATETIME_FORMATTING),
            'last_name': obj.last_name,
            'first_name': obj.first_name,
            'middle_name': obj.middle_name,
            'sex': obj.sex,
            'pk': str(obj.pk),  # todo ##fixme##
        })
