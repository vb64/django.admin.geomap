"""Test urls.

make test T=test_urls.py
"""
from django.urls import reverse
from . import TestBase


class TestsUrls(TestBase):
    """Url tests.

    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#admin-reverse-urls
    """

    def test_home(self):
        """Root page."""
        response = self.client.get(reverse('home'))
        assert response.status_code == 200

    def test_admin(self):
        """Admin site urls."""
        from django.contrib.auth.models import User  # pylint: disable=imported-auth-user

        password = 'mypassword'
        admin = User.objects.create_superuser('admin_test_suite', 'myemail@test.com', password)
        self.client.login(username=admin.username, password=password)

        response = self.client.get(reverse('admin:index'))
        assert response.status_code == 200

        response = self.client.get(reverse('admin:example_location_changelist'))
        assert response.status_code == 200

        response = self.client.get(reverse('admin:example_location_add'))
        assert response.status_code == 200

        from example.models import Location

        location = Location(
          name='First location'
        )
        location.save()

        response = self.client.get(reverse('admin:example_location_change', args=(location.id,)))
        assert response.status_code == 200

        location.lon = 0.0
        location.lat = 0.0
        location.save()

        response = self.client.get(reverse('admin:example_location_change', args=(location.id,)))
        assert response.status_code == 200
