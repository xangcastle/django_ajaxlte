# ajaxlte


# Requirements
* Python = 3
* Django >= 3.05
* django-crispy-forms >= 1.9.0

# Installation

* ```pip install django-grappelli-extras```

## settings.py

 * Put 'grappelli_extras' **before** 'grappelli' on INSTALLED_APPS

```python
# Your setting will look like:
INSTALLED_APPS = [
    'ajaxlte',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # continue with your apps
]
```

* Put 'applist' in your active context_processors.
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```


## urls.py

 * Put grappelli extras urls in 'urlpatterns':

```python
# Your urls will look like:
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ajalte/', include('ajaxlte.urls')),
]
```


Available features:

* [class based views](#classview)
Rewritable methods for class based views.

* [adminlte 3.0](#adminlte)
Using adminlte template 3.0.

* [Traslation](#translation)
Traslation Suport by Locales.
