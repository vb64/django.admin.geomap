"""Django url views."""
from django.http import HttpResponse


def home(request):
    """Main page."""
    return HttpResponse("Hi")
