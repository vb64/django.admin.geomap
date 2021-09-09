"""Admin site."""
from django.contrib import admin
from django_admin_geomap import ModelAdmin

from .models import Location


class Admin(ModelAdmin):
    """Admin site customization."""

    list_display = ['name', 'lon', 'lat']


admin.site.register(Location, Admin)
