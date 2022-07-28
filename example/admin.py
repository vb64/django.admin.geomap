"""Admin site."""
from django.contrib import admin
from django_admin_geomap import ModelAdmin

from .models import Location


class Admin(ModelAdmin):
    """Admin site customization."""

    list_display = ['name', 'lon', 'lat']
    geomap_field_longitude = "id_lon"
    geomap_field_latitude = "id_lat"
    search_fields = ['name']


admin.site.register(Location, Admin)
