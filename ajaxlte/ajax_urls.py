from django.urls import path
from .ajax import *

app_name = "ajaxlte"

urlpatterns = [
    path('get_object/', get_object, name="getObject"),
    path('object_update/', object_update, name="ObjectUpdate"),
    path('object_view/', object_view, name="ObjectView"),
    path('get_collection/', get_collection, name="getCollection"),
    path('get_datatables/', get_datatables, name="getDataTables"),
    path('autocomplete/', autocomplete, name="autocomplete"),
    path('object_execute/', object_execute, name="objectExecute"),
    path('get_html_form/', get_html_form, name="getHtmlForm"),
]
