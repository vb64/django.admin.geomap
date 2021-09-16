"""Django url views."""
from django.shortcuts import render
from django_admin_geomap import fill_geomap_context

from .models import Location


def home(request):
    """Main page."""
    context = {
      'geomap_items': Location.objects.all()
    }
    fill_geomap_context(context)

    return render(request, 'example_home.html', context)
