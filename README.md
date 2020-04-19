# ajaxlte

Available features:

* [class based views](#classview)
Rewritable methods for class based views.

* [adminlte 3.0](#adminlte)
Using adminlte template 3.0.

* [Traslation](#translation)
Traslation Suport by Locales.


# Requirements
* Python = 3
* Django >= 3.05
* django-crispy-forms >= 1.9.0

# Installation

* ```pip install django-ajaxlte```

## settings.py

 * Add 'ajaxlte' in your INSTALLED_APPS.

```python
INSTALLED_APPS = [
    'ajaxlte',
    ...
]
```


## urls.py

 * Put grappelli extras urls in 'urlpatterns':

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ajax/', include('ajaxlte.ajax_urls')),
]
```



# How to use

In your models.py import BaseModel and use like parent.

```python
from django.db import models
from ajaxlte.models import BaseModel


class Foo(BaseModel):
    code = models.CharField(max_length=35, null=True, blank=True)
    name = models.CharField(max_length=165, null=True, blank=True)

    def __str__(self):
        return self.code


class Bar(BaseModel):
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)
    code = models.CharField(max_length=35, null=True, blank=True)
    name = models.CharField(max_length=165, null=True, blank=True)

    def __str__(self):
        return self.code
```


In your views.py

```python
from ajaxlte.generics import Index, Datatables, AjaxSite
from .models import *


# creating de index page
class TestIndex(Index):
    proyect_name = "proyect name"
    site = AjaxSite


# creating the foo datatable
class FooDatatable(Datatables):
    site = AjaxSite
    model = Foo
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


# add index site
AjaxSite.name_space = "testapp"
AjaxSite.set_index(TestIndex)


# add menu
AjaxSite.add_pill('test1')


# register classes
AjaxSite.register(FooDatatable, 'test1')
# 'test1' is the name of the menu than you want to put this module
```