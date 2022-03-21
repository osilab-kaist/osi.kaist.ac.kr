from django.contrib import admin

# Register your models here.
from core.models import User, Publication, Photo, Project, InvitationCode, Award


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):
    pass
