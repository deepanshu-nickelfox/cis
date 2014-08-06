from django.conf.urls import patterns, url, include
from api.v1 import urls as api_v1_urls
from api.v2 import urls as api_v2_urls

urlpatterns = patterns('',
    url(r'v1/', include(api_v1_urls)),
    url(r'v2/', include(api_v2_urls)),
)
