"""Models definition."""
from django.db import models


class Location(models.Model):
    name = models.CharField()
    lon = models.FloatField()
    lat = models.FloatField()
