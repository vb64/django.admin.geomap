"""Models definition."""
from django.db import models
from django_admin_geomap import GeoItem


class Location(models.Model, GeoItem):

    name = models.CharField(max_length=100)
    lon = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def geomap_longitude(self):
        return '' if self.lon is None else str(self.lon)

    @property
    def geomap_latitude(self):
        return '' if self.lat is None else str(self.lat)
