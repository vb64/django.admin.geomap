"""Geomap package."""
from html import escape
from django.contrib import admin


class Key:
    """Parameters for Django template."""

    CenterLongitude = 'geomap_longitude'
    CenterLatitude = 'geomap_latitude'
    MapZoom = 'geomap_zoom'
    MapHeight = 'geomap_height'
    IsEditor = 'geomap_edit'
    NewIcon = 'geomap_new_feature_icon'
    IsForm = 'geomap_form'
    FieldLongitude = 'geomap_field_longitude'
    FieldLatitude = 'geomap_field_latitude'
    MapItems = 'geomap_items'
    AutoZoom = 'geomap_autozoom'


class GeoItem:
    """Mixing class for model with geomap support."""

    default_icon = "https://maps.google.com/mapfiles/ms/micons/red.png"

    @property
    def geomap_popup_view(self):
        """Html code for display in marker popup at the map for RO users."""
        return "<strong>{}</strong>".format(escape(str(self), quote=True))

    @property
    def geomap_popup_edit(self):
        """Html code for display in marker popup at the map for admin users."""
        return self.geomap_popup_view

    @property
    def geomap_popup_common(self):
        """Html code for display in marker popup at the map for common views."""
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
    geomap_autozoom = "-1"
    geomap_show_map_on_list = True

    geomap_field_longitude = ""
    geomap_field_latitude = ""

    add_form_template = 'geomap/add_form.html'
    change_form_template = 'geomap/change_form.html'
    change_list_template = 'geomap/changelist.html'

    def set_common(self, request, context):
        """Set common map properties."""
        context = context or {}
        context.update(geomap_context(
          None,
          map_longitude=self.geomap_default_longitude,
          map_latitude=self.geomap_default_latitude,
          map_zoom=self.geomap_default_zoom,
          auto_zoom=self.geomap_autozoom,
          map_height=self.geomap_height
        ))
        context[Key.IsEditor] = self.has_change_permission(request)
        context[Key.NewIcon] = self.geomap_new_feature_icon
        context[Key.IsForm] = self.geomap_field_longitude and self.geomap_field_latitude
        context[Key.FieldLongitude] = self.geomap_field_longitude
        context[Key.FieldLatitude] = self.geomap_field_latitude

        return context

    def changelist_view(self, request, extra_context=None):
        """Add geomap data to show at the map."""
        # Obtain original response from Django
        response = super().changelist_view(request, extra_context=extra_context)

        if not self.geomap_show_map_on_list:
            return response

        if (not hasattr(response, 'context_data')) or ('cl' not in response.context_data):
            return response

        # Obtain final queryset from ChangeList object
        change_list_queryset = response.context_data['cl'].queryset

        # Add the geomap data to the context
        extra_context = self.set_common(request, extra_context)
        extra_context[Key.MapItems] = change_list_queryset
        response.context_data.update(extra_context)  # add to existing context

        return response

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add data for show item at the map."""
        extra_context = self.set_common(request, extra_context)
        item = list(self.get_queryset(request).filter(id=int(object_id)))[0]

        if item.geomap_longitude and item.geomap_latitude:
            extra_context[Key.MapItems] = [item]
            extra_context[Key.CenterLongitude] = item.geomap_longitude
            extra_context[Key.CenterLatitude] = item.geomap_latitude
            extra_context[Key.MapZoom] = self.geomap_item_zoom

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        """New antenna data at the map."""
        return super().add_view(request, form_url, extra_context=self.set_common(request, extra_context))


def geomap_context(
  objects,
  map_longitude="0.0",
  map_latitude="0.0",
  map_zoom="1",
  auto_zoom="-1",
  map_height="500px"
):
    """Fill context with geomap defaults."""
    return {
      Key.CenterLongitude: map_longitude,
      Key.CenterLatitude: map_latitude,
      Key.MapZoom: map_zoom,
      Key.AutoZoom: auto_zoom,
      Key.MapHeight: map_height,
      Key.MapItems: objects or []
    }
