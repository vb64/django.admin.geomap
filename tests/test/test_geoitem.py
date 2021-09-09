"""Test GeoItem class.

make test T=test_geoitem.py
"""
import pytest
from . import TestBase


class TestsGeoItem(TestBase):
    """GeoItem class."""

    @staticmethod
    def test_properties():
        """Check properties."""
        from example.models import Location

        name = 'Test location'
        location = Location(name=name)
        location.save()

        assert 'red.png' in location.geomap_icon
        assert name in location.geomap_popup_view
        assert name in location.geomap_popup_edit
        assert location.geomap_latitude == ''
        assert location.geomap_longitude == ''

        location.lon = 0.0
        location.lat = 10.0
        location.save()

        assert location.geomap_longitude == '0.0'
        assert location.geomap_latitude == '10.0'

    @staticmethod
    def test_exception():
        """Check NotImplementedError."""
        from django_admin_geomap import GeoItem

        item = GeoItem()

        with pytest.raises(NotImplementedError) as err:
            item.geomap_longitude  # pylint: disable=pointless-statement
        assert 'geomap_longitude' in str(err.value)

        with pytest.raises(NotImplementedError) as err:
            item.geomap_latitude  # pylint: disable=pointless-statement
        assert 'geomap_latitude' in str(err.value)
