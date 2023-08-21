from collections import defaultdict
from datetime import timedelta, datetime

import django.contrib.auth.views
from django.conf import settings
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, ListView, DeleteView

from core.forms import PublicationForm, AdminPublicationForm, AdminProjectForm, ProjectForm, AdminPhotoForm, SignupForm, \
    ProfileForm, PhotoFormWithoutImage, PhotoForm, AdminAwardForm, AwardForm, GPUStatusForm, PostForm, PasswordResetForm
from core.mixins import JsonableResponseMixin, MemberRequiredMixin, PhdRequiredMixin, StaffRequiredMixin
from core.models import Publication, Project, Photo, User, Award, PublicationTag, GPUStatus, Post


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = dict()
        user = self.request.user
        if user.is_authenticated:
            now = timezone.localtime(timezone.now())
            if 0 <= now.hour < 5 or 17 <= now.hour:
                greeting = "Good evening"
            elif 5 <= now.hour < 12:
                greeting = "Good morning"
            else:
                greeting = "Good afternoon"

            greeting += ", "
            if user.position == "PRO":
                greeting += "Professor {}".format(user.last_name)
            else:
                greeting += user.first_name
            greeting += "!"
            context["greeting"] = greeting

        all_posts = Post.objects.order_by("-published_date").all()
        latest_posts = []
        for post in all_posts:
            if len(latest_posts) < 3 or post.published_date > (datetime.now() - timedelta(days=3 * 30)).date():
                latest_posts.append(post)
            else:
                break
        context["latest_posts"] = latest_posts
        return context


class ProfessorView(TemplateView):
    template_name = "core/professor.html"


class StudentsView(TemplateView):
    template_name = "core/people.html"

    def get_context_data(self, **kwargs):
        now = timezone.now()
        context = dict()
        context["postdocs"] = User.objects.filter(position="POS").exclude(position_end_date__lt=now).order_by(
            'position_start_date', 'first_name').all()
        phd_students = User.objects.filter(position__in=["PHD", "INT"]).exclude(
            position_end_date__lt=now).order_by('position_start_date', 'first_name').all()
        phd_students = [
            (s.position_start_date if s.position == "PHD" else s.position_start_date + timedelta(days=365), s.name, s)
            for s in phd_students
        ]
        phd_students.sort()
        phd_students = [s[2] for s in phd_students]
        context["phd_students"] = phd_students
        context["ms_students"] = User.objects.filter(position="MAS").exclude(position_end_date__lt=now).exclude(
            profile_image='').order_by('position_start_date', 'first_name').all()
        context["visiting_students"] = User.objects.filter(position="VIS").exclude(position_end_date__lt=now).exclude(
            profile_image='').order_by('position_start_date', 'first_name').all()
        context["alumni_students"] = User.objects.filter(position__in=["PHD", "INT", "MAS"],
                                                         position_end_date__lt=timezone.now()).order_by(
            'position_end_date', 'first_name').all()
        context["past_visitors"] = User.objects.filter(position="VIS").filter(
            position_end_date__lt=now).exclude(
            profile_image='').order_by('position_start_date', 'first_name').all()
        return context


class PublicationsView(TemplateView):
    template_name = "core/publications.html"

    def get_context_data(self, **kwargs):
        publications = Publication.objects.filter(type__in=["CON", "WOR", "JRN"], public=True).order_by(
            '-published_date', 'authors').prefetch_related("tags").all()
        unpublished_publications = Publication.objects.filter(type__in=["CON", "WOR", "JRN"], public=False).order_by(
            '-published_date', 'authors').prefetch_related("tags").all()
        domestic_publications = Publication.objects.filter(type__in=["KCO", "KJR"]).order_by(
            '-published_date', 'authors').prefetch_related("tags").all()
        publications = list(publications)

        # Add indices
        conference_index = 1
        workshop_index = 1
        journal_index = 1
        for p in publications[::-1]:
            if p.type == "CON":
                p.index = "C{}".format(conference_index)
                conference_index += 1
            elif p.type == "WOR":
                p.index = "W{}".format(workshop_index)
                workshop_index += 1
            elif p.type == "JRN":
                p.index = "J{}".format(journal_index)
                journal_index += 1

        # Organize by year
        publications_by_year = defaultdict(list)
        for p in publications:
            p: Publication
            publications_by_year[p.published_date.year].append(p)
        publications_by_year = [{
            "year": year,
            "publications": publications,
        } for year, publications in publications_by_year.items()]

        context = dict()
        context["publications"] = publications_by_year
        context["unpublished_publications"] = unpublished_publications
        context["domestic_publications"] = domestic_publications

        years = set()
        for pub in publications:
            years.add(pub.published_date.year)

        context["years"] = list(sorted(list(years), reverse=True))
        context["types"] = [
            ('JRN', 'Journal'),
            ('CON', 'Conference'),
            ('WOR', 'Workshop'),
        ]
        context["research_areas"] = PublicationTag.objects.order_by("name").all()

        return context


class ProjectsView(TemplateView):
    template_name = "core/projects.html"

    def get_context_data(self, **kwargs):
        context = dict()
        context["unpublished_projects"] = Project.objects.filter(public=False).order_by("-priority", "start_date").all()
        context["active_projects"] = Project.objects.filter(end_date__gte=timezone.now(), public=True).order_by(
            "-priority", "start_date").all()
        context["past_projects"] = Project.objects.filter(end_date__lt=timezone.now(), public=True).order_by(
            "-priority", "start_date").all()
        return context


class AwardsView(TemplateView):
    template_name = "core/awards.html"

    def get_context_data(self, **kwargs):
        context = dict()
        context["awards"] = Award.objects.filter(public=True).order_by('-awarded_date', 'awardees').all()
        context["unpublished_awards"] = Award.objects.filter(public=False).order_by('-awarded_date', 'awardees').all()
        return context


class ApplyView(TemplateView):
    template_name = "core/apply.html"


class PhotosView(TemplateView):
    template_name = "core/photos.html"

    def get_context_data(self, **kwargs):
        context = dict()
        photos = Photo.objects.order_by("-public", "taken_date").all()
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
        return context


class NewsView(ListView):
    template_name = "core/news.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.order_by("-published_date")


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

        form.invitation_code.uses_remaining -= 1
        form.invitation_code.save()
        form.save()

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password1"]
        user = authenticate(username=email, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse("home"))


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "core/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("students")

    def get_object(self, queryset=None):
        return self.request.user


class PublicationCreateView(MemberRequiredMixin, CreateView):
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


class PublicationUpdateView(MemberRequiredMixin, UpdateView):
    template_name = "core/publication_update.html"
    object: Publication
    model = Publication
    slug_field = "id"
    success_url = reverse_lazy("publications")

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminPublicationForm
        else:
            return PublicationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PublicationDeleteView(StaffRequiredMixin, DeleteView):
    template_name = "core/publication_delete.html"
    model = Publication
    slug_field = "id"
    success_url = reverse_lazy("publications")


class ProjectCreateView(PhdRequiredMixin, CreateView):
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


class ProjectUpdateView(PhdRequiredMixin, UpdateView):
    template_name = "core/project_update.html"
    model = Project
    slug_field = "id"
    success_url = reverse_lazy("projects")

    object: Project

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminProjectForm
        else:
            return ProjectForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectDeleteView(StaffRequiredMixin, DeleteView):
    template_name = "core/project_delete.html"
    model = Project
    slug_field = "id"
    success_url = reverse_lazy("projects")


class AwardCreateView(MemberRequiredMixin, CreateView):
    template_name = "core/award_create.html"
    model = Award
    success_url = reverse_lazy("awards")

    object: Award

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminAwardForm
        else:
            return AwardForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AwardUpdateView(MemberRequiredMixin, UpdateView):
    template_name = "core/award_update.html"
    model = Award
    slug_field = "id"
    success_url = reverse_lazy("awards")

    object: Award

    def get_form_class(self):
        if self.request.user.is_staff:
            return AdminAwardForm
        else:
            return AwardForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostCreateView(PhdRequiredMixin, CreateView):
    template_name = "core/post_create.html"
    model = Post
    success_url = reverse_lazy("news")
    form_class = PostForm

    object: Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostUpdateView(PhdRequiredMixin, UpdateView):
    template_name = "core/post_update.html"
    model = Post
    slug_field = "id"
    success_url = reverse_lazy("news")
    form_class = PostForm

    object: Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostDeleteView(StaffRequiredMixin, DeleteView):
    template_name = "core/post_delete.html"
    model = Post
    slug_field = "id"
    success_url = reverse_lazy("news")


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
    slug_field = "id"
    success_url = reverse_lazy("photos")

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
        self.object.last_modified_by = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PhotoDeleteView(StaffRequiredMixin, DeleteView):
    template_name = "core/photo_delete.html"
    model = Photo
    slug_field = "id"
    success_url = reverse_lazy("photos")


class ResetPasswordView(SuccessURLAllowedHostsMixin, FormView):
    template_name = "core/reset_password.html"
    form_class = PasswordResetForm
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def form_valid(self, form):
        user = form.save(commit=True)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(csrf_exempt, name='dispatch')
class GPUStatusCreateAPIView(JsonableResponseMixin, CreateView):
    model = GPUStatus
    form_class = GPUStatusForm
    success_url = "/"
