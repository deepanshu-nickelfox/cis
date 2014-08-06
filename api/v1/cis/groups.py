from django.contrib.auth.models import Group
from api.v1.cis.permissions import PermissionsResource
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource


class GroupsResource(ModelResource):

    permissions = fields.ToManyField(
        PermissionsResource, 'permissions', full=True, null=True)

    class Meta:
        queryset = Group.objects.all()
        resource_name = 'groups'
        authentication = SessionAuthentication()
        # Everyone can read the list of groups
        authorization = DjangoAuthorization()
        always_return_data = True
        # Disallow put and patch to list, because they are poorly implemented
        # in tastypie
        list_allowed_methods = ['get', 'post', 'delete']
        max_limit = 0
        limit = 0
