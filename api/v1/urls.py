from django.conf.urls import patterns, url, include
from api.v1.cis.auth import AuthResource
from api.v1.cis.permissions import PermissionsResource
from api.v1.hr.users import UsersResource

auth_resource = AuthResource()
users_resource = UsersResource()
permissions_resource = PermissionsResource()

urlpatterns = patterns('',
    url(r'', include(auth_resource.urls)),
    url(r'', include(users_resource.urls)),
    url(r'', include(permissions_resource.urls)),
)
