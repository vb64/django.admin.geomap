# DjangoAdminGeomap library
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/django.admin.geomap/geomap-pep257?label=Pep257&style=plastic)](https://github.com/vb64/django.admin.geomap/actions?query=workflow%3Ageomap-pep257)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/vb64/django.admin.geomap/geomap-tests?label=Django%203.2.5&style=plastic)](https://github.com/vb64/django.admin.geomap/actions?query=workflow%3Ageomap-tests)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/d565c3a3d78e4e198f35688432a741eb)](https://www.codacy.com/gh/vb64/django.admin.geomap/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vb64/django.admin.geomap&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/d565c3a3d78e4e198f35688432a741eb)](https://www.codacy.com/gh/vb64/django.admin.geomap/dashboard?utm_source=github.com&utm_medium=referral&utm_content=vb64/django.admin.geomap&utm_campaign=Badge_Coverage)

The free, open-source DjangoAdminGeomap library is designed to display objects on the map in the Django admin site.

![objects on the map in the Django admin site](img/listchange.png)

There is a full-fledged multifunctional GIS framework [GeoDjango](https://docs.djangoproject.com/en/3.2/ref/contrib/gis/).
When is used in the Django admin site, you can display objects on the map.
However, GeoDjango has a large [list of dependencies](https://docs.djangoproject.com/en/3.2/ref/contrib/gis/install/#requirements) on various libraries
and the specifics of installing these libraries on various platforms.

If you only need to display objects on the map in the Django admin site, then you can use the DjangoAdminGeomap library.
It has no additional requirements for the names and data types of fields in the database tables, and there are no installation dependencies.

DjangoAdminGeomap uses the [OpenLayers](https://openlayers.org/) JavaScript framework to display map data.
The source of the cartographic data is the data of the [OpenStreetMap project](https://www.openstreetmap.org/).

## Installation

```bash
pip install django-admin-geomap
```

After installation, you need to plug the library into your Django project by making changes to the `settings.py` file.

## Changes to settings.py

To connect DjangoAdminGeomap to your project, you need to add to the file `settings.py` in the key` TEMPLATES` the path to the directory `templates` of the library.

```python
TEMPLATES = [
  {
    'DIRS': ['path/to/installed/django_admin_geomap/templates'],
  },
]
```

An example of such a connection can be found in the file [example/settings.py](https://github.com/vb64/django.admin.geomap/blob/3fb078d231517f368158ff4fd2c63c11092af979/example/settings.py#L43).

It is not necessary to include the library in the `INSTALLED_APPS` list in` settings.py`.

## Initial data

Let's say we have a table in the database, the records of which contain data about coordinates.

```python
# models.py
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    lon = models.FloatField()  # longitude
    lat = models.FloatField()  # latitude

```

When working with this table in the admin panel, we want to see a map with objects from this table located on it.

## Displaying a list of objects on the map

To enable the display of `Location` objects on the map in the Django admin panel, you need to make changes to the model class in the` models.py` file and to the `admin.py` file.

Add the django_admin_geomap.GeoItem "mixin" class to the inheritance list of the `Location` class and define two properties:` geomap_longitude` and `geomap_latitude`.
These properties should return the longitude and latitude of the object as a string.

```python
# models.py
from django.db import models
from django_admin_geomap import GeoItem

class Location(models.Model, GeoItem):

    @property
    def geomap_longitude(self):
        return str(self.lon)

    @property
    def geomap_latitude(self):
        return str(self.lat)
```

In the `admin.py` file, when registering a model, you need to use the` django_admin_geomap.ModelAdmin` class.

```python
# admin.py
from django.contrib import admin
from django_admin_geomap import ModelAdmin
from .models import Location

admin.site.register(Location, ModelAdmin)
```

After making these changes, in the admin panel on the page with a list of `Location` objects, a map with markers at the locations of these objects will be displayed under the table.

## Displaying the object on the map in the edit form

To display an object on the map in the edit/view form, you must additionally specify the field IDs in the Django form, which contain the longitude and latitude values of the object.

For our `Location` class, the Django admin automatically assigns the IDs` id_lon` and `id_lat` to these form fields. The following changes need to be made to the `admin.py` file.

```python
# admin.py
from django.contrib import admin
from django_admin_geomap import ModelAdmin
from .models import Location

class Admin(ModelAdmin):
    geomap_field_longitude = "id_lon"
    geomap_field_latitude = "id_lat"

admin.site.register(Location, Admin)
```

After making these changes, in the admin panel on the page for viewing/editing the `Location` object, a map with a marker at the location of the object will be displayed.

When editing, you can change the position of an object by dragging its icon across the map with the mouse (you need to move the mouse cursor over the bottom of the icon until a blue dot appears on it).

When adding a new object, its position can be set by clicking on the map. Further, the marker of the new object can be dragged, similar to editing.

## Additional customization

The library allows you to customize the view of the map and objects by setting special properties for the model class and the `django_admin_geomap.ModelAdmin` class.

### Object icon on the map

The `geomap_icon` property of the model class sets the path to the marker icon. You can use different icons depending on the state of a particular object.

The default is `https://maps.google.com/mapfiles/ms/micons/red.png`.

```python
# models.py
from django.db import models
from django_admin_geomap import GeoItem

class Location(models.Model, GeoItem):

    @property
    def geomap_icon(self):
        return self.default_icon
```

### Text in a pop-up block when you click on a marker on the map

The properties `geomap_popup_view` and `geomap_popup_edit` for the model class set the HTML code that is used in the pop-up block when the mouse is clicked on the marker on the map.
The `geomap_popup_view` property specifies the code for a user without permission to edit the object, and the` geomap_popup_edit` property - for a user who has permission to edit.

By default, both properties return the string representation of the object.

```python
# models.py
from django.db import models
from django_admin_geomap import GeoItem

class Location(models.Model, GeoItem):

    @property
    def geomap_popup_view(self):
        return "<strong>{}</strong>".format(str(self))

    @property
    def geomap_popup_edit(self):
        return self.geomap_popup_view
```

### New object marker icon

The `geomap_new_feature_icon` property of the` django_admin_geomap.ModelAdmin` class sets the path to the marker icon when adding a new object.

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_new_feature_icon = "/myicon.png"
```

### Zoom level and center of the map when displaying a list of objects

You can change the zoom level and position of the center of the map by setting the properties `geomap_default_longitude`,` geomap_default_latitude` and `geomap_default_zoom` in the class` django_admin_geomap.ModelAdmin`.

By default, the center of the map is located at the point with coordinates "0.0", "0.0" and the scale is "1".

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_default_longitude = "95.1849"
    geomap_default_latitude = "64.2637"
    geomap_default_zoom = "3"
```

### Map zoom when editing/viewing an object

In object edit form the center of the map coincides with the location of the object. The zoom level of the map can be set by using the `geomap_item_zoom` property of the `django_admin_geomap.ModelAdmin` class.

The default is "13".

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_item_zoom = "10"
```

### Vertical map size

When displayed, the map occupies the maximum possible horizontal size. The vertical size can be set via the `geomap_height` property of the `django_admin_geomap.ModelAdmin` class.
The value must be a string valid in the CSS style definition.

The default is "500px".

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_height = "300px"
```
