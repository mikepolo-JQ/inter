from django.contrib import admin

from src.applications.smart.models import Match


@admin.register(Match)
class MatchAdminModel(admin.ModelAdmin):
    pass
