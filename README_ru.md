# Библиотека GeoMap

Бесплатная, с открытым исходным кодом библиотека GeoMap предназначена для отображения обьектов на карте в админке Django.

Существует проект [GeoDjango](https://docs.djangoproject.com/en/3.2/ref/contrib/gis/), решающий в т.ч. и эту задачу. 
GeoDjango является полноценным многофункциональным ГИС фреймворком.
По этой причине он имеет большой [список зависимостей](https://docs.djangoproject.com/en/3.2/ref/contrib/gis/install/#requirements) от различных библиотек
и особенности установки этих библиотек на различных платформах.

Если нам требуется только отображение обьектов на карте в админке Django, то можно использовать библиотеку GeoMap. 
У GeoMap нет дополнительных требований к именам и типам данных полей в таблицах базы данных и отсутствуют зависимости при установке.

Для отображения картографических данных GeoMap использует JavaScript фреймворк [OpenLayers](https://openlayers.org/).
Источником картографических данных являются данные проекта [OpenStreetMap](https://www.openstreetmap.org/).

## Установка GeoMap

```
pip install django-admin-geomap
```

После установки нужно подключить GeoMap к вашему проекту Django, внеся изменения в файл `settings.py`.

## Изменения в settings.py

Для подключения GeoMap к вашему проекту нужно добавить в файл `settings.py` в ключ `TEMPLATES` путь на каталог `templates` библиотеки.

```python
TEMPLATES = [
  {
    'DIRS': ['path/to/installed/geomap/templates'],
  },
]
```

Включать библиотеку в список `INSTALLED_APPS` в `settings.py` не требуется.

## Исходные данные

Допустим, у нас в БД имеется таблица, записи которой содержат данные о координатах.

```python
from django.db import models

class Location(models.Model):
    name = models.CharField()
    lon = models.FloatField()  # долгота
    lat = models.FloatField()  # широта

```

При работе с этой таблицей в админке мы хотим видеть карту с расположенными на ней обьектами из этой таблицы.

## Отображение списка обьектов на карте

```python
# models.py
from django.db import models
from geomap import GeoItem

class Location(models.Model, GeoItem):

    @property
    def geomap_longitude(self):
        return str(self.lon)

    @property
    def geomap_latitude(self):
        return str(self.lat)
```

```python
# admin.py
from django.contrib import admin
from geomap import ModelAdmin
from .models import Location

admin.site.register(Location, ModelAdmin)
```

## Отображение редактируемого/добавляемого обьекта на карте

```python
# admin.py
from django.contrib import admin
from geomap import ModelAdmin
from .models import Location

class Admin(ModelAdmin):
    geomap_field_longitude = "id_lon"
    geomap_field_latitude = "id_lat"

admin.site.register(Location, Admin)
```

## Дополнительные настройки

```python
# admin.py
from django.contrib import admin
from geomap import ModelAdmin
from .models import Location

class Admin(ModelAdmin):
    geomap_field_longitude = "id_lon"
    geomap_field_latitude = "id_lat"

    geomap_new_feature_icon = GeoItem.default_icon
    geomap_default_longitude = "95.1849"
    geomap_default_latitude = "64.2637"
    geomap_default_zoom = "3"
    geomap_item_zoom = "13"
    geomap_height = "500px"

admin.site.register(Location, Admin)
```

```python
# models.py
from django.db import models
from geomap import GeoItem

class Location(models.Model, GeoItem):

    @property
    def geomap_popup_view(self):
        return "<strong>{}</strong>".format(str(self))

    @property
    def geomap_popup_edit(self):
        return self.geomap_popup_view

    @property
    def geomap_icon(self):
        return self.default_icon
```
