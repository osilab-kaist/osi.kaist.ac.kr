from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'ongoing', views.ongoing_projects, name="on-going projects"),
    url(r'past', views.past_projects, name="on-going projects")
]


