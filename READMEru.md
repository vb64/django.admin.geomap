# Библиотека DjangoAdminGeomap

[На английском](README.md)

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

Для подключения DjangoAdminGeomap к вашему проекту в файле `settings.py` нужно добавить `'django_admin_geomap'` в `INSTALLED_APPS`.

```python

INSTALLED_APPS = (

...

  'django_admin_geomap',
)
```

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

Если хотя бы одно из этих двух свойств возвращает пустую строку, то соответствующий объект не будет отображаться на карте.
Например, объекты у которых отсутсвуют координаты или какие то "секретные" объекты из вашей БД.

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
        return '' if self.lat is None else str(self.lat)
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
В качестве обязательного аргумента функции нужно передать итерируемую последовательность производных от класса `django_admin_geomap.GeoItem` объектов для отображения на карте.
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

-   map_longitude: долгота центра карты, по умолчанию "0.0"
-   map_latitude: широта центра карты, по умолчанию "0.0"
-   map_zoom: масштаб карты, по умолчанию "1"
-   auto_zoom: включает режим автозуммирования (см. ниже), по умолчанию "-1" (режим автозуммирования отключен)
-   map_height: размер карты по вертикали, по умолчанию "500px"

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

## Режим автозуммирования

По умолчанию данный режим отключен.
Вы можете включить режим автозуммирования при отображении объектов на карте как в обычных вьюшках, так и в админке Django.

В обычных вьюшках Django в функцию `geomap_context` нужно передать именованный аргумент `auto_zoom`.

```python
    return render(request, 'home.html', geomap_context(Location.objects.all(), auto_zoom="10"))
```

В классе админки нужно задать атрибут `geomap_autozoom`.

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_autozoom = "10"
```

Режим автозуммирования работает по разному в зависимости от количества объектов, которые нужно отобразить на карте.

Если список отображаемых объектов пустой, то режим автозуммирования отключается.

Если в списке содержится один объект, то центр карты устанавливается в координаты этого объекта, а масштаб карты устанавливается в значение параметра автозуммирования (10 для примеров выше).

Если в списке содержится более одного объекта, программа определяет минимальный прямоугольник, вмещающий все отображаемые объекты.
Центр карты устанавливается в координаты центра этого прямоугольник.
Масштаб карты устанавливается таким образом, чтобы вместить данный прямоугольник с небольшими отступами по краям.

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

При клике мышью по маркеру на карте отображается всплывающий блок. Используемый в этом блоке HTML код можно задать, определив три свойства у класса модели.

-   `geomap_popup_common` отображается в регулярных представлениях (views)
-   `geomap_popup_view` отображается в админке для пользователя без прав на изменение объекта
-   `geomap_popup_edit` отображается в админке для пользователя, который имеет права на редактирование

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

### Отключение карты при отображении списка объектов в админке

При отображении списка объектов в админке по умолчанию карта со значками обьектов отображается.
Чтобы скрыть карту, установите свойство `geomap_show_map_on_list` класса `django_admin_geomap.ModelAdmin` в `False`.

```python
# admin.py
from django_admin_geomap import ModelAdmin

class Admin(ModelAdmin):
    geomap_show_map_on_list = False
```

## Пример использования

Вы можете запустить работающий на локальном компьютере пример использования библиотеки.

На платформе Windows для этого нужно предварительно установить следующие программы.

-   [Python3](https://www.python.org/downloads/release/python-3810/)
-   GNU [Unix Utils](http://unxutils.sourceforge.net/) для операций через makefile
-   [Git for Windows](https://git-scm.com/download/win) для доступа к репозитарию исходных кодов.

Затем склонировать репозитарий и запустить установку, указав путь на Python 3.

```bash
git clone git@github.com:vb64/django.admin.geomap.git
cd django.admin.geomap
make setup PYTHON_BIN=/usr/bin/python3
```

Собрать файлы медиа и создать базу данных.

```bash
make static
make db
```

Создать суперюзера базы данных, указав для него логин и пароль.

```bash
make superuser
```

Запустить пример.

```bash
make example
```

Открыть в браузере адрес `http://127.0.0.1:8000/` для просмотра сайта примера.
Для входа в админку `http://127.0.0.1:8000/admin/` нужно использовать логин и пароль, заданные при создании суперюзера.
