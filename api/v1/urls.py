from django.conf.urls import patterns, url, include
from api.v1.cis.auth import AuthResource
from api.v1.cis.groups import GroupsResource
from api.v1.cis.permissions import PermissionsResource
from api.v1.cis.users import UsersResource
from api.v1.hr.positions import PositionsResource

auth_resource = AuthResource()
users_resource = UsersResource()
permissions_resource = PermissionsResource()
groups_resource = GroupsResource()
positions_resource = PositionsResource()

urlpatterns = patterns('',
    url(r'', include(auth_resource.urls)),
    url(r'', include(users_resource.urls)),
    url(r'', include(permissions_resource.urls)),
    url(r'', include(groups_resource.urls)),
    url(r'', include(positions_resource.urls)),
)
