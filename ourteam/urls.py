from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'professor', views.display_professor, name="professor"),
    url(r'students', views.display_students, name="students"),
    url(r'alumni', views.display_alumni, name="alumni")
]


