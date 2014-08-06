from django.conf.urls import patterns, url, include
from api.v1 import urls as api_v1_urls

urlpatterns = patterns('',
    url(r'v1/', include(api_v1_urls)),
)
