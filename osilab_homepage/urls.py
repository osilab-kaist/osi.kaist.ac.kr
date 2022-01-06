from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.views.static import serve
from django.urls import re_path
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', include('home.urls')),
    url(r'^ourteam/', include('ourteam.urls')),
    url(r'^publications/', include('publications.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^seminar/', include('seminar.urls')),
    url(r'^photo/', include('photo.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    url(r'^$', include('home.urls')),
]
