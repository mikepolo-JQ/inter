from django.contrib import admin

from profile.models import Profile


@admin.register(Profile)
class ProfileAdminModel(admin.ModelAdmin):
    pass
