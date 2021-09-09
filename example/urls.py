"""Django url router."""
from django.conf.urls import url
from django.contrib import admin
from .views import home

urlpatterns = [  # pylint: disable=invalid-name
  url(r'^$', home, name='home'),
  url(r'^admin/', admin.site.urls),
]
