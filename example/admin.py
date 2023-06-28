"""Admin site."""
from django.contrib import admin
from django_admin_geomap import ModelAdmin

from .models import Location, LocationUuid


class Admin(ModelAdmin):
    """Admin site customization."""

    list_display = ['name', 'lon', 'lat']
    geomap_field_longitude = "id_lon"
    geomap_field_latitude = "id_lat"
    search_fields = ['name']
    geomap_item_zoom  = "10"
    geomap_autozoom = geomap_item_zoom


class AdminUuid(Admin):
    """Admin site for uuid model."""

    list_display = ['name', 'longitude', 'latitude']
    geomap_field_longitude = "id_longitude"
    geomap_field_latitude = "id_latitude"
    search_fields = ['name']
    geomap_item_zoom  = "10"
    geomap_autozoom = geomap_item_zoom


admin.site.register(Location, Admin)
admin.site.register(LocationUuid, AdminUuid)
