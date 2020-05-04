# ajaxlte

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

[![Latest PyPI version](https://img.shields.io/pypi/v/django-ajaxlte.svg)](https://crate.io/packages/django-ajaxlte/)

[![Number of PyPI downloads](https://img.shields.io/pypi/l/django-ajaxlte.svg)](https://crate.io/packages/django-ajaxlte/)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)

[![PyPI download month](https://img.shields.io/pypi/dm/django-ajaxlte.svg)](https://pypi.python.org/pypi/django-ajaxlte/)

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
    ...,
    'django.contrib.humanize',
    'mathfilters',
    'crispy_forms',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    ...,
    'ajaxlte.middleware.JSONParsingMiddleware',
    'ajaxlte.middleware.PutParsingMiddleware',
    'ajaxlte.middleware.DeleteParsingMiddleware',
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
from django.shortcuts import render


# this is a public website, maybe your root url
def website(request):
    return render(request, 'testapp/index.html')


# general settings
AjaxSite.proyect_name = "Amazing proyect"
AjaxSite.name_space = "testapp"
AjaxSite.root_url = "testapp/"
AjaxSite.login_url = "/admin/login/"
AjaxSite.logo_url = "/static/testapp/img/logo.png"
AjaxSite.spinner = "/static/testapp/img/spinner.gif" # the spinner is the gif loaded between ajax requests


# creating de index page
class TestIndex(Index):
    site = AjaxSite


# creating the foo datatable
class FooDatatable(Datatables):
    site = AjaxSite
    model = Foo
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


# creating the foo datatable
class Bars(Datatables):
    site = AjaxSite
    model = Bar
    list_display = ('code', 'name', 'foo')
    search_fields = ('code', 'name')


# add index site
AjaxSite.set_index(TestIndex)


# add menu
AjaxSite.add_pill('test1')
AjaxSite.add_pill('test2')


# register classes
AjaxSite.register(FooDatatable, 'test1')
AjaxSite.register(Bars, 'test2')
```


In your main urls.py include ajaxlte and your AjaxSite.

```python
from django.contrib import admin
from django.urls import path, include
from testapp.views import AjaxSite, website

urlpatterns = [
    path('', website, name="website"),
    path(AjaxSite.root_url, include((AjaxSite.urlpatterns, AjaxSite.name_space), namespace=AjaxSite.name_space)),
    path('admin/', admin.site.urls),
    path('ajax/', include('ajaxlte.ajax_urls')),
]

```