"""Django url views."""
from django.shortcuts import render
from django_admin_geomap import geomap_context

from .models import Location, LocationUuid


def home(request):
    """Main page."""
    return render(request, 'example_home.html', geomap_context(Location.objects.all()))


def home_uuid(request):
    """Page with uuid-key locations."""
    return render(request, 'example_home.html', geomap_context(LocationUuid.objects.all()))
