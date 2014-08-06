from django.contrib.auth import get_user_model
from tastypie.test import ResourceTestCase


class Test(ResourceTestCase):

    def setUp(self):
        super(Test, self).setUp()
        get_user_model().objects.create_user('test', 'test')

    def test_login(self):
        login_url = '/api/v2/auth/login/'
        resp = self.api_client.post(login_url, data={'email': 'test', 'password': 'test'})
        self.assertHttpOK(resp)
        self.assertIn('_auth_user_id', self.api_client.client.session)

    def test_logout_must_be_logged_in(self):
        logout_url = '/api/v2/auth/logout/'
        resp = self.api_client.get(logout_url)
        self.assertHttpUnauthorized(resp)

    def test_logout(self):
        logout_url = '/api/v2/auth/logout/'
        self.api_client.client.login(email='test', password='test')
        resp = self.api_client.get(logout_url)
        self.assertHttpOK(resp)
        self.assertNotIn('_auth_user_id', self.api_client.client.session)
