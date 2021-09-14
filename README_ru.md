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

В файле `admin.py` при регистрации модели нужно использовать класс `django_admin_geomap.ModelAdmin`.

```python
# admin.py
from django.contrib import admin
from django_admin_geomap import ModelAdmin
from .models import Location

admin.site.register(Location, ModelAdmin)
```

После внесения данных изменений в админке на странице со списком обьектов `Location` под таблицей будет отображаться карта с маркерами в местах расположения этих обьектов.

## Отображение редактируемого/добавляемого обьекта на карте

Для отображения на карте обьекта в форме редактирования/просмотра необходимо дополнительно указать ID полей в форме Django, в которых находятся значения долготы и широты обьекта.

Для нашего класса `Location` админка Django автоматически присваивает полям формы ID `id_lon` и `id_lat`. В файл `admin.py` нужно внести следующие изменения.

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

После внесения данных изменений в админке на странице просмотра/редактирования обьекта `Location` будет отображаться карта с маркером в месте расположения обьекта.

При редактировании можно менять положение обьекта, перетаскивая его значок по карте при помощи мыши (нужно навести курсор мыши на нижнюю часть значка до появления на нем синей точки).

При добавлении нового обьекта его положение можно задать кликом на карте. Далее маркер нового обьекта можно перетаскивать, аналогично редактированию.

## Дополнительные настройки

Библиотека GeoMap позволяет делать дополнительные настройки отображения карты и обьектов, задавая специальные свойства у класса модели и класса административного интерфейса `django_admin_geomap.ModelAdmin`.

### Значок маркера обьекта на карте

Свойство `geomap_icon` у класса модели задает путь на значок маркера. Можно использовать разные значки в зависимости от состояния конкретного обьекта.

По умолчанию используется строка `https://maps.google.com/mapfiles/ms/micons/red.png`

```python
# models.py
from django.db import models
from django_admin_geomap import GeoItem

class Location(models.Model, GeoItem):

    @property
    def geomap_icon(self):
        return self.default_icon
```

### Текст во всплывающем блоке при клике мышью по маркеру на карте

Свойства `geomap_popup_view` и `geomap_popup_edit` у класса модели задают HTML код, который используется во всплывающем блоке при клике мышью по маркеру на карте.
Свойство `geomap_popup_view` задает код для отображения пользователю без прав на изменения обьекта, а свойство `geomap_popup_edit` - для пользователя, который имеет права на редактирование.

По умолчанию оба свойства используют строковое представление обьекта.

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

### Значок маркера нового обьекта

Свойство `geomap_new_feature_icon` класса `django_admin_geomap.ModelAdmin` задает путь на значок маркера при добавлении нового обьекта.

По умолчанию используется значок для отображения обьектов на карте.

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_new_feature_icon = "/myicon.png"
```

### Масштаб и центр карты при отображении списка обьектов

Вы можете менять масштаб и положение центра карты, задавая свойства `geomap_default_longitude`, `geomap_default_latitude` и `geomap_default_zoom` у класса `django_admin_geomap.ModelAdmin`.

По умолчанию центр карты располагается в точке с координатами "0.0", "0.0" и используется масштаб "1".

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_default_longitude = "95.1849"
    geomap_default_latitude = "64.2637"
    geomap_default_zoom = "3"
```

### Масштаб карты при редактировании/просмотре обьекта

При редактировании/просмотре обьекта центр карты сопадает с местом расположения обьекта, а масштаб карты можно задать, используя свойство `geomap_item_zoom` у класса `django_admin_geomap.ModelAdmin`.

По умолчанию этот масштаб равен "13".

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_item_zoom = "10"
```

### Размер карты по вертикали

При отображении карты ее размер по горизонтали принимает максимально возможное значение, а размер по вертикали можно задать через свойство `geomap_height` у класса `django_admin_geomap.ModelAdmin`.
Значение должно быть строкой, допустимой в определении CSS стиля.

По умолчанию "500px".

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_height = "300px"
```
