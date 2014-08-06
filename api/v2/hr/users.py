from django.contrib.auth import get_user_model
from api.v2.authorization import ReadRestrictedDjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource


class UsersResource(ModelResource):
    class Meta:
        queryset = get_user_model().objects.all()
        resource_name = 'users'
        excludes = ['password']
        authentication = SessionAuthentication()
        authorization = ReadRestrictedDjangoAuthorization()
        always_return_data = True
        # Disallow put and patch to list, because they are poorly implemented
        # in tastypie
        list_allowed_methods = ['get', 'post', 'delete']

