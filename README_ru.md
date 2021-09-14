# Библиотека GeoMap

Бесплатная, с открытым исходным кодом библиотека GeoMap предназначена для отображения обьектов на карте в админке Django.

![Обьекты на карте в админке Django](img/listchange01.jpg)

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

Пример такого подключения можно посмотреть в файле [example/settings.py](https://github.com/vb64/django.admin.geomap/blob/3fb078d231517f368158ff4fd2c63c11092af979/example/settings.py#L43).

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

Чтобы включить отображение обьектов `Location` на карте в админке Django нужно внести изменения в класс модели в файле `models.py` и в файл настроек админки `admin.py`.

В список наследования класса `Location` нужно добавить "примесный" класс `GeoItem` из библиотеки GeoMap и определить два свойства: `geomap_longitude` и `geomap_latitude`.
Эти свойства должны возвращать долготу и широту обьекта в виде строки.

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

В файле `admin.py` нужно при регистрации модели нужно использовать класс ModelAdmin из библиотеки GeoMap.

```python
# admin.py
from django.contrib import admin
from django_admin_geomap import ModelAdmin
from .models import Location

admin.site.register(Location, ModelAdmin)
```

После внесения данных изменений в админке на странице со списком обьектов `Location` под таблицей будет отображаться карта с маркерами в местах расположения этих обьектов.

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
