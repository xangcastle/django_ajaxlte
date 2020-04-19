from ajaxlte.generics import Index, Datatables, AjaxSite
from .forms import *


class TestIndex(Index):
    company_name = "tecnolite"
    site = AjaxSite


class Foos(Datatables):
    site = AjaxSite
    model = Foo
    form = FooForm
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


class Bars(Datatables):
    site = AjaxSite
    model = Bar
    list_display = ('code', 'name', 'foo')
    search_fields = ('code', 'name')


# add index site
AjaxSite.name_space = "testapp"
AjaxSite.set_index(TestIndex)


# add menu
AjaxSite.add_pill('test1')
AjaxSite.add_pill('test2')


# register classes
AjaxSite.register(Foos, 'test1')
AjaxSite.register(Bars, 'test2')


