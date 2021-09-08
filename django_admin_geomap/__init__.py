"""Geomap package."""
from django.contrib import admin


class GeoItem:
    """Mixing class for model with geomap support."""

    default_icon = "https://maps.google.com/mapfiles/ms/micons/red.png"

    @property
    def geomap_popup_view(self):
        """Html code for display in marker popup at the map for RO users."""
        return "<strong>{}</strong>".format(str(self))

    @property
    def geomap_popup_edit(self):
        """Html code for display in marker popup at the map for admin users."""
        return self.geomap_popup_view

    @property
    def geomap_icon(self):
        """Full url for marker icon at the map."""
        return self.default_icon

    @property
    def geomap_longitude(self):
        """Must return longitude of object as string."""
        raise NotImplementedError("{}.geomap_longitude".format(self.__class__.__name__))

    @property
    def geomap_latitude(self):
        """Must return latitude of object as string."""
        raise NotImplementedError("{}.geomap_latitude".format(self.__class__.__name__))


class ModelAdmin(admin.ModelAdmin):
    """Base class for admin model with geomap support."""

    geomap_new_feature_icon = GeoItem.default_icon
    geomap_default_longitude = "0.0"
    geomap_default_latitude = "0.0"
    geomap_default_zoom = "1"
    geomap_item_zoom = "13"
    geomap_height = "500px"

    geomap_field_longitude = ""
    geomap_field_latitude = ""

    add_form_template = 'geomap/add_form.html'
    change_form_template = 'geomap/change_form.html'
    change_list_template = 'geomap/changelist.html'

    def set_common(self, request, extra_context):
        """Set common map properties."""
        extra_context = extra_context or {}
        extra_context['geomap_edit'] = self.has_change_permission(request)
        extra_context['geomap_new_feature_icon'] = self.geomap_new_feature_icon
        extra_context['geomap_longitude'] = self.geomap_default_longitude
        extra_context['geomap_latitude'] = self.geomap_default_latitude
        extra_context['geomap_zoom'] = self.geomap_default_zoom
        extra_context['geomap_height'] = self.geomap_height
        extra_context['geomap_form'] = self.geomap_field_longitude and self.geomap_field_latitude
        extra_context['geomap_field_longitude'] = self.geomap_field_longitude
        extra_context['geomap_field_latitude'] = self.geomap_field_latitude

        return extra_context

    def changelist_view(self, request, extra_context=None):
        """Add geomap data for show at the map."""
        extra_context = self.set_common(request, extra_context)
        extra_context['geomap_items'] = self.get_queryset(request)

        return super().changelist_view(request, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add data for show item at the map."""
        extra_context = self.set_common(request, extra_context)
        item = list(self.get_queryset(request).filter(id=int(object_id)))[0]

        if item.geomap_longitude and item.geomap_latitude:
            extra_context['geomap_items'] = [item]
            extra_context['geomap_longitude'] = item.geomap_longitude
            extra_context['geomap_latitude'] = item.geomap_latitude
            extra_context['geomap_zoom'] = self.geomap_item_zoom

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        """New antenna data at the map."""
        return super().add_view(request, form_url, extra_context=self.set_common(request, extra_context))
