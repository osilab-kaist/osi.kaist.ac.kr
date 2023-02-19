from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("professor/", views.ProfessorView.as_view(), name="professor"),
    path("students/", views.StudentsView.as_view(), name="students"),
    path("publications/", views.PublicationsView.as_view(), name="publications"),
    path("projects/", views.ProjectsView.as_view(), name="projects"),
    path("awards/", views.AwardsView.as_view(), name="awards"),
    path("news/", views.NewsView.as_view(), name="news"),
    path("apply/", views.ApplyView.as_view(), name="apply"),
    path("photos/", views.PhotosView.as_view(), name="photos"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("profile/", views.ProfileView.as_view(), name="profile"),

    path("project/create/", views.ProjectCreateView.as_view(), name="project_create"),
    path("project/<slug:slug>/update/", views.ProjectUpdateView.as_view(), name="project_update"),
    path("project/<slug:slug>/delete/", views.ProjectDeleteView.as_view(), name="project_delete"),
    path("publication/create/", views.PublicationCreateView.as_view(), name="publication_create"),
    path("publication/<slug:slug>/update/", views.PublicationUpdateView.as_view(), name="publication_update"),
    path("publication/<slug:slug>/delete/", views.PublicationDeleteView.as_view(), name="publication_delete"),
    path("award/create/", views.AwardCreateView.as_view(), name="award_create"),
    path("award/<slug:slug>/update/", views.AwardUpdateView.as_view(), name="award_update"),
    path("post/create/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("photo/create/", views.PhotoCreateView.as_view(), name="photo_create"),
    path("photo/<slug:slug>/update/", views.PhotoUpdateView.as_view(), name="photo_update"),
    path("photo/<slug:slug>/delete/", views.PhotoDeleteView.as_view(), name="photo_delete"),

    path("api/gpu-status/create/", views.GPUStatusCreateAPIView.as_view(), name="gpu_status_create_api"),

    path("reset-password", views.ResetPasswordView.as_view(), name="reset_password"),

    path("", views.HomeView.as_view(), name="home"),
]
