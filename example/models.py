"""Models definition."""
import uuid

from django.db import models
from django_admin_geomap import GeoItem


class Location(models.Model, GeoItem):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

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


class WithQuotas(Location):
    """Model with quotas."""

    def __str__(self):
        """Quotas in string representation."""
        return "\"{}\"".format(self.name)
