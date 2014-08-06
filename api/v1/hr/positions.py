from api.v1.authorization import ReadRestrictedDjangoAuthorization
from api.v1.cis.groups import GroupsResource
from hr.models import Position
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource


class PositionsResource(ModelResource):

    department = fields.ToOneField(
        GroupsResource, 'department', full=True, null=True)

    class Meta:
        queryset = Position.objects.all()
        resource_name = 'positions'
        authentication = SessionAuthentication()
        authorization = ReadRestrictedDjangoAuthorization()
        always_return_data = True
        # Disallow put and patch to list, because they are poorly implemented
        # in tastypie
        list_allowed_methods = ['get', 'post', 'delete']

