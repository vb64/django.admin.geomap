"""Django url router."""
from django.urls import path
from django.contrib import admin
from .views import home

urlpatterns = [  # pylint: disable=invalid-name
  path('', home, name='home'),
  path('admin/', admin.site.urls),
]
