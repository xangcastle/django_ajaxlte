from django.contrib import admin
from django.urls import path, include
from testapp.views import AjaxSite, website

urlpatterns = [
    path('', website, name="website"),
    path(AjaxSite.root_url, include((AjaxSite.urlpatterns, AjaxSite.name_space), namespace=AjaxSite.name_space)),
    path('admin/', admin.site.urls),
    path('ajax/', include('ajaxlte.ajax_urls')),
]
