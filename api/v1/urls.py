from django.conf.urls import patterns, url, include
from rest_framework import routers
from api.v1.cis.groups import GroupViewSet
from api.v1.cis.users import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = patterns('',
    url(r'', include(router.urls, namespace='api-v1')),
)
