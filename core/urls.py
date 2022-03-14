from django.urls import path

from . import views

urlpatterns = [
    path("professor/", views.display_professor, name="professor"),
    path("students/", views.display_students, name="students"),
    path("alumni/", views.display_alumni, name="alumni"),
    path("photo/<int:year>/", views.photo, name="photo"),
    path("ongoing/", views.ongoing_projects, name="projects_ongoing"),
    path("past/", views.past_projects, name="projects_past"),
    path("conference/", views.conference, name="publications_conference"),
    path("journal/", views.journal, name="publications_journal"),
    path("patents/", views.patent, name="publications_patents"),
    path("", views.home, name="home"),
]
