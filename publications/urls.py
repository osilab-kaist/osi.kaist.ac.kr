from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'conference', views.conference, name="conference"),
    url(r'journal', views.journal, name="conference"),
    url(r'patents', views.patent, name="conference"),
]



