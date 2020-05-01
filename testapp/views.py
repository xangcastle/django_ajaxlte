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
AjaxSite.spinner = "/static/testapp/img/spinner.gif"


# creating de index page
class TestIndex(Index):
    site = AjaxSite


# creating the foo datatable
class FooDatatable(Datatables):
    site = AjaxSite
    model = Foo
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


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


