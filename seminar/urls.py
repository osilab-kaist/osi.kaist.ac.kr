from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'past', views.past_seminar, name="past seminar"),
    url(r'thisweek', views.seminar, name="this week seminar"),
    url(r'', views.seminar, name="seminar"),
]


