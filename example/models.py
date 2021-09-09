"""Models definition."""
from django.db import models
from django_admin_geomap import GeoItem


class Location(models.Model, GeoItem):
    name = models.CharField(max_length=100)
    lon = models.FloatField()
    lat = models.FloatField()

    @property
    def geomap_longitude(self):
        return str(self.lon)

    @property
    def geomap_latitude(self):
        return str(self.lat)
