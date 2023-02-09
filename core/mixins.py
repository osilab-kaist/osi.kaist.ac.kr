from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse

from core.models import User


class RequestType:
    """For code-inspection
    """
    user: User


class JsonableResponseMixin:
    """
    Based on example from Django 3.2

    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        data = {
            'id': self.object.id,
        }
        return JsonResponse(data)


class PhdRequiredMixin(UserPassesTestMixin):
    request: RequestType

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.has_phd_permissions


class MemberRequiredMixin(UserPassesTestMixin):
    request: RequestType

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.has_member_permissions


class StaffRequiredMixin(UserPassesTestMixin):
    request: RequestType

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
