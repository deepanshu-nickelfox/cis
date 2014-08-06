from django.conf.urls import patterns, url, include
from api.v2.cis.auth import AuthResource
from api.v2.hr.users import UsersResource

auth_resource = AuthResource()
users_resource = UsersResource()

urlpatterns = patterns('',
    url(r'', include(auth_resource.urls)),
    url(r'', include(users_resource.urls)),
)
