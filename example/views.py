"""Django url views."""
from django.shortcuts import render


def home(request):
    """Main page."""
    return render(request, 'example_home.html', {})
