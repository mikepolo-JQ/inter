from django.contrib import admin

from smart.models import Match


@admin.register(Match)
class MatchAdminModel(admin.ModelAdmin):
    pass