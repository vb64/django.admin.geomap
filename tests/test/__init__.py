"""Root class for testing."""
from django.test import TestCase, Client


class TestBase(TestCase):
    """Base class for tests."""

    def setUp(self):
        """Set up Django client."""
        super().setUp()
        self.client = Client()
