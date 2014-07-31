from django.conf.urls import patterns, url, include
from rest_framework import routers
from api.v1.cis.groups import GroupViewSet
from api.v1.cis.login import LoginView
from api.v1.cis.users import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = patterns('',
    url(r'', include(router.urls, namespace='api-v1')),
    url(r'login/$', LoginView().as_view(), name='api-v1-login'),
)
