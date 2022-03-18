from collections import defaultdict

import django.contrib.auth.views
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, FormView, CreateView, UpdateView

from core.forms import PublicationForm, AdminPublicationForm, AdminProjectForm, ProjectForm, AdminPhotoForm, SignupForm, \
    ProfileForm, PhotoFormWithoutImage, PhotoForm
from core.models import Publication, Project, Photo, User


class HomeView(TemplateView):
    template_name = "core/home.html"


class ProfessorView(TemplateView):
    template_name = "core/professor.html"


class StudentsView(TemplateView):
    template_name = "core/students.html"

    def get_context_data(self, **kwargs):
        context = dict()
        context["phd_students"] = User.objects.filter(position="PHD", profile_image__isnull=False, position_end_date__gte=timezone.now()).order_by('-position_start_date', 'first_name').all()
        context["integrated_students"] = User.objects.filter(position="INT", profile_image__isnull=False, position_end_date__gte=timezone.now()).order_by('-position_start_date', 'first_name').all()
        context["ms_students"] = User.objects.filter(position="MAS", profile_image__isnull=False, position_end_date__gte=timezone.now()).order_by('-position_start_date', 'first_name').all()
        context["visiting_students"] = User.objects.filter(position="VIS", profile_image__isnull=False, position_end_date__gte=timezone.now()).order_by('-position_start_date', 'first_name').all()
        context["alumni_students"] = User.objects.filter(position__in=["PHD", "INT", "MAS"],  position_end_date__lt=timezone.now()).order_by('-position_end_date', 'first_name').all()
        return context


class PublicationsView(TemplateView):
    template_name = "core/publications.html"

    def get_context_data(self, **kwargs):
        context = dict()
        context["publications"] = Publication.objects.filter(type__in=["CON", "WOR", "JRN"], public=True).order_by('-published_date', 'authors').all()
        context["unpublished_publications"] = Publication.objects.filter(type__in=["CON", "COW", "JRN"], public=False).order_by('-published_date', 'authors').all()
        context["domestic_publications"] = Publication.objects.filter(type__in=["KCO", "KJR"]).order_by('-published_date', 'authors').all()
        return context


class ProjectsView(TemplateView):
    template_name = "core/projects.html"

    def get_context_data(self, **kwargs):
        context = dict()
        context["unpublished_projects"] = Project.objects.filter(public=False).order_by("start_date").all()
        context["active_projects"] = Project.objects.filter(end_date__gte=timezone.now(), public=True).order_by("start_date").all()
        context["past_projects"] = Project.objects.filter(end_date__lt=timezone.now(), public=True).order_by("start_date").all()
        return context


class PhotosView(TemplateView):
    template_name = "core/photos.html"

    def get_context_data(self, **kwargs):
        context = dict()
        photos = Photo.objects.filter(public=True).order_by('taken_date').all()
        unpubished_photos = Photo.objects.filter(public=False).all()
        photos_by_year = defaultdict(list)
        for p in photos:
            photos_by_year[p.taken_date.year].append(p)
        photos_by_year_list = list()
        for year in reversed(sorted(photos_by_year.keys())):
            photos_by_year_list.append({
                "year": year,
                "photos": photos_by_year[year],
            })
        context["photos"] = photos_by_year_list
        context["unpublished_photos"] = unpubished_photos
        return context


class RequestType:
    """For code-inspection
    """
    user: User


class LoginView(django.contrib.auth.views.LoginView):
    redirect_authenticated_user = True
    template_name = "core/login.html"


class SignupView(FormView):
    template_name = "core/signup.html"
    form_class = SignupForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse("home"))
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.position = form.invitation_code.position
        user.save()
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        user = authenticate(username=email, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse("home"))


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "core/profile.html"
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user


class PhdRequiredMixin(UserPassesTestMixin):
    request: RequestType

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.has_phd_permissions


class MemberRequiredMixin(UserPassesTestMixin):
    request: RequestType

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.has_member_permissions


class PublicationCreateView(PhdRequiredMixin, CreateView):
    template_name = "core/publication_create.html"
    object: Publication
    model = Publication
    success_url = reverse_lazy("publications")

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminPublicationForm
        else:
            return PublicationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PublicationUpdateView(PhdRequiredMixin, UpdateView):
    template_name = "core/publication_update.html"
    object: Publication
    model = Publication
    success_url = reverse_lazy("publications")
    slug_field = "id"

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminPublicationForm
        else:
            return PublicationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectCreateView(MemberRequiredMixin, CreateView):
    template_name = "core/project_create.html"
    model = Project
    success_url = reverse_lazy("projects")

    object: Project

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminProjectForm
        else:
            return ProjectForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdateView(MemberRequiredMixin, UpdateView):
    template_name = "core/project_update.html"
    model = Project
    success_url = reverse_lazy("projects")
    slug_field = "id"

    object: Project

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminProjectForm
        else:
            return ProjectForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PhotoCreateView(MemberRequiredMixin, CreateView):
    template_name = "core/photo_create.html"
    model = Photo
    success_url = reverse_lazy("photos")

    object: Photo

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminPhotoForm
        else:
            return PhotoForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PhotoUpdateView(MemberRequiredMixin, UpdateView):
    template_name = "core/photo_update.html"
    model = Photo
    success_url = reverse_lazy("photos")
    slug_field = "id"

    object: Photo

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminPhotoForm
        else:
            if self.object.public:
                return PhotoFormWithoutImage
            else:
                return PhotoForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
