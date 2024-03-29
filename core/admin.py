from django.contrib import admin
from django.db.models.functions import Lower

# Register your models here.
from core.models import User, Publication, Photo, Project, InvitationCode, Award, PublicationTag, AdminToken, GPUStatus, \
    Post, PasswordResetToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("__str__", "first_name", "last_name", "email", "position", "position_start_date", "id")
    ordering = [Lower("last_name")]


@admin.register(PublicationTag)
class PublicationTagAdmin(admin.ModelAdmin):
    exclude = ["last_modified_by"]

    def save_model(self, request, obj, form, change):
        obj.last_modified_by = request.user
        super().save_model(request, obj, form, change)


def make_public(modeladmin, request, queryset):
    queryset.update(public=True)


make_public.short_description = 'Mark selected content as public'


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "authors", "venue", "published_date", "created_date")
    list_filter = ("type",)

    actions = [make_public]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("__str__", "members", "organization", "start_date", "end_date")

    actions = [make_public]


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ("name", "awardees", "venue", "awarded_date", "created_date")

    actions = [make_public]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "created_date")

    actions = [make_public]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "created_by", "created_date", "image")

    actions = [make_public]


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token")


@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(AdminToken)
class AdminTokenAdmin(admin.ModelAdmin):
    pass


@admin.register(GPUStatus)
class GPUStatusAdmin(admin.ModelAdmin):
    pass
