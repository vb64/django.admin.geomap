"""Django url views."""
from django.shortcuts import render
from django_admin_geomap import geomap_context

from .models import Location


def home(request):
    """Main page."""
    return render(request, 'example_home.html', geomap_context(Location.objects.all()))
