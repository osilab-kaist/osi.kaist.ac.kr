from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.views.static import serve
from django.urls import re_path
from django.conf import settings

urlpatterns = [
    url('', include('core.urls')),
    url(r'^admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
]
