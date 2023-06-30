from django.contrib import admin

from learning.squads.models import Squad


class SquadAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(Squad, SquadAdmin)
