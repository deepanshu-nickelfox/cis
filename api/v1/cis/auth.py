from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from tastypie.http import HttpForbidden, HttpUnauthorized
from tastypie.resources import Resource
from tastypie.utils import trailing_slash


class AuthResource(Resource):

    class Meta:
        resource_name = 'auth'
        authentication = SessionAuthentication()
        authorization = Authorization()
        allowed_methods = ['get', 'post']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(
            request,
            request.body,
            format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('email', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {
                'success': True
            })
        else:
            return self.create_response(request, {
                'success': False
            }, HttpUnauthorized)
