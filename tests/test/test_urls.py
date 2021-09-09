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
        admin = User.objects.create_superuser('admin', 'myemail@test.com', password)
        self.client.login(username=admin.username, password=password)

        response = self.client.get(reverse('admin:index'))
        assert response.status_code == 200
