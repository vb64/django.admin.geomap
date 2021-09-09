"""Admin site."""
from django.contrib import admin
from .models import Location


class Admin(admin.ModelAdmin):
    """Admin site customization."""

    list_display = ['name', 'lon', 'lat']


admin.site.register(Location, Admin)
