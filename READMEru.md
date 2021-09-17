# Библиотека DjangoAdminGeomap

Бесплатная, с открытым исходным кодом библиотека DjangoAdminGeomap предназначена для отображения объектов на карте в представлениях (views) и админке Django.

![объекты на карте в админке Django](img/listchange01.jpg)

Существует полноценный многофункциональный ГИС фреймворк [GeoDjango](https://docs.djangoproject.com/en/3.2/ref/contrib/gis/).
При его использовании в админке Django можно отображать объекты на карте.
Однако GeoDjango имеет большой [список зависимостей](https://docs.djangoproject.com/en/3.2/ref/contrib/gis/install/#requirements) от различных библиотек
и особенности установки этих библиотек на различных платформах.

Если вам требуется только отображение объектов на карте в админке Django, то можно использовать библиотеку DjangoAdminGeomap. 
У нее нет дополнительных требований к именам и типам данных полей в таблицах базы данных и отсутствуют зависимости при установке.

Для отображения картографических данных DjangoAdminGeomap использует JavaScript фреймворк [OpenLayers](https://openlayers.org/).
Источником картографических данных являются данные проекта [OpenStreetMap](https://www.openstreetmap.org/).

## Установка

```bash
pip install django-admin-geomap
```

После установки нужно подключить библиотеку к вашему проекту Django, внеся изменения в файл `settings.py`.

## Изменения в settings.py

Для подключения DjangoAdminGeomap к вашему проекту нужно добавить в файл `settings.py` в ключ `TEMPLATES` путь на каталог `templates` библиотеки.

```python
TEMPLATES = [
  {
    'DIRS': ['path/to/installed/django_admin_geomap/templates'],
  },
]
```

Пример такого подключения можно посмотреть в файле [example/settings.py](https://github.com/vb64/django.admin.geomap/blob/3fb078d231517f368158ff4fd2c63c11092af979/example/settings.py#L43).

Включать библиотеку в список `INSTALLED_APPS` в `settings.py` не нужно.

## Исходные данные

Допустим, у нас в БД имеется таблица, записи которой содержат данные о координатах.

```python
# models.py
from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    lon = models.FloatField()  # долгота
    lat = models.FloatField()  # широта

```

На главной странице сайта и при работе с этой таблицей в админке мы хотим видеть карту с расположенными на ней объектами из этой таблицы.

## Главная страница со списком объектов на карте 

Чтобы включить отображение объектов `Location` на карте нужно внести изменения в класс модели в файле `models.py`.

В список наследования класса `Location` нужно добавить "примесный" класс `django_admin_geomap.GeoItem` и определить два свойства: `geomap_longitude` и `geomap_latitude`.
Эти свойства должны возвращать долготу и широту объекта в виде строки.

```python
# models.py
from django.db import models
from django_admin_geomap import GeoItem

class Location(models.Model, GeoItem):

    @property
    def geomap_longitude(self):
        return '' if self.lon is None else str(self.lon)

    @property
    def geomap_latitude(self):
        return '' if self.lon is None else str(self.lat)
```

После внесения данных изменений в определение модели можно отображать карту с объектами из таблицы `Location` в произвольном представлении (view).
Для этого в шаблон станицы нужно включить файл `geomap/common.html`. Например, шаблон корневой страницы сайта `home.html` может выглядеть так:

```html
<!DOCTYPE html>
<html lang="en">

<head>
<title>DjangoAdminGeomap example</title>
</head>

<body>
Hello, OpenStreetMap!
<div>{% include "geomap/common.html" %}</div>
</body>

</html>
```

В функции представления нужно передавать в этот шаблон контекст, сформированный вызовом функции `geomap_context`.
В качестве обязательного аргумента функции нужно передать итерируемую последовательность объектов для отображения на карте.
Например, список или Django QuerySet.

```python
# views.py
from django.shortcuts import render
from django_admin_geomap import geomap_context

from .models import Location


def home(request):
    return render(request, 'home.html', geomap_context(Location.objects.all()))
```

На корневой странице сайта будет отображаться карта с маркерами в местах расположения этих объектов.

Функция `geomap_context` принимает дополнительные именованные аргументы, позволяющие настроить свойства карты.

- map_longitude: долгота центра карты, по умолчанию "0.0"
- map_latitude: широта центра карты, по умолчанию "0.0"
- map_zoom: масштаб карты, по умолчанию "1"
- map_height: размер карты по вертикали, по умолчанию "500px"

## Cписок объектов на карте в админке

Для отображения карты с обьектами в админке сайта в файле настроек админки `admin.py` при регистрации модели нужно использовать класс `django_admin_geomap.ModelAdmin`.

```python
# admin.py
from django.contrib import admin
from django_admin_geomap import ModelAdmin
from .models import Location

admin.site.register(Location, ModelAdmin)
```

После внесения данных изменений в админке на странице со списком объектов `Location` под таблицей будет отображаться карта с маркерами в местах расположения этих объектов.

## Отображение редактируемого объекта на карте в админке

Для отображения на карте объекта в форме редактирования/просмотра необходимо дополнительно указать идентификаторы полей в форме Django, в которых находятся значения долготы и широты объекта.

Для нашего класса `Location` админка Django автоматически присваивает этим полям формы идентификаторы `id_lon` и `id_lat`. В файл `admin.py` нужно внести следующие изменения.

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

После внесения данных изменений в админке на странице просмотра/редактирования объекта `Location` будет отображаться карта с маркером в месте расположения объекта.

При редактировании можно менять положение объекта, перетаскивая его значок по карте при помощи мыши (нужно навести курсор мыши на нижнюю часть значка до появления на нем синей точки).

При добавлении нового объекта его положение можно задать кликом на карте. Далее маркер нового объекта можно перетаскивать, аналогично редактированию.

## Дополнительные настройки

Библиотека позволяет настраивать вид карты и объектов, задавая специальные свойства у класса модели и класса `django_admin_geomap.ModelAdmin`.

### Значок маркера объекта на карте

Свойство `geomap_icon` у класса модели задает путь на значок маркера. Можно использовать разные значки в зависимости от состояния конкретного объекта.

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

При клике мышью по маркеру на карте отображается всплывающем блоке. Используемый в этом блоке HTML код можно задать, определив три свойства у класса модели.

- `geomap_popup_common` отображается в регулярных представлениях (views)
- `geomap_popup_view` отображается в админке для пользователя без прав на изменение объекта
- `geomap_popup_edit` отображается в админке для пользователя, который имеет права на редактирование

По умолчанию все свойства возвращают строковое представление объекта.

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

    @property
    def geomap_popup_common(self):
        return self.geomap_popup_view
```

### Значок маркера нового объекта

Свойство `geomap_new_feature_icon` класса `django_admin_geomap.ModelAdmin` задает путь на значок маркера при добавлении нового объекта в админке Django.

По умолчанию используется значок для отображения объектов на карте.

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_new_feature_icon = "/myicon.png"
```

### Масштаб и центр карты при отображении списка объектов в админке

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

### Масштаб карты при редактировании/просмотре объекта в админке

При редактировании/просмотре объекта центр карты совпадает с местом расположения объекта, а масштаб карты можно задать, используя свойство `geomap_item_zoom` у класса `django_admin_geomap.ModelAdmin`.

По умолчанию этот масштаб равен "13".

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_item_zoom = "10"
```

### Размер карты по вертикали в админке

При отображении карта занимает максимально возможный размер по горизонтали, а размер по вертикали можно задать через свойство `geomap_height` у класса `django_admin_geomap.ModelAdmin`.
Значение должно быть строкой, допустимой в определении CSS стиля.

По умолчанию "500px".

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_height = "300px"
```
