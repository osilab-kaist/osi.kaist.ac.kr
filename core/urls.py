from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("professor/", views.ProfessorView.as_view(), name="professor"),
    path("students/", views.StudentsView.as_view(), name="students"),
    path("publications/", views.PublicationsView.as_view(), name="publications"),
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("awards/", views.AwardsView.as_view(), name="awards"),
    path("photos/", views.PhotosView.as_view(), name="photos"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("profile/", views.ProfileView.as_view(), name="profile"),

    path("project/create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("project/<slug:slug>/update/", views.ProjectUpdateView.as_view(), name="project_update"),
    path("publication/create/", views.PublicationCreateView.as_view(), name="publication_create"),
    path("publication/<slug:slug>/update/", views.PublicationUpdateView.as_view(), name="publication_update"),
    path("award/create/", views.AwardCreateView.as_view(), name="award_create"),
    path("award/<slug:slug>/update/", views.AwardUpdateView.as_view(), name="award_update"),
    path("photo/create/", views.PhotoCreateView.as_view(), name="photo_create"),
    path("photo/<slug:slug>/update/", views.PhotoUpdateView.as_view(), name="photo_update"),

    path("api/gpu-status/create/", views.GPUStatusCreateAPIView.as_view(), name="gpu_status_create_api"),

    path("", views.HomeView.as_view(), name="home"),
]
