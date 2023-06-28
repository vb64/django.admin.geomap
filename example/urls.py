"""Django url router."""
from django.urls import path
from django.contrib import admin
from .views import home, home_uuid

urlpatterns = [  # pylint: disable=invalid-name
  path('', home, name='home'),
  path('uuid/', home_uuid, name='home_uuid'),
  path('admin/', admin.site.urls),
]
