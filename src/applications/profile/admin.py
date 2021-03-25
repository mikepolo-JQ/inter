from django.contrib import admin

from src.applications.profile.models import Profile


@admin.register(Profile)
class ProfileAdminModel(admin.ModelAdmin):
    pass
