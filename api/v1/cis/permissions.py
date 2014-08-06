from django.contrib.auth.models import Permission
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource


class PermissionsResource(ModelResource):
    class Meta:
        queryset = Permission.objects.all()
        resource_name = 'permissions'
        authentication = SessionAuthentication()
        # Everyone can read the list of permissions
        authorization = DjangoAuthorization()
        always_return_data = True
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        max_limit = 0
        limit = 0
