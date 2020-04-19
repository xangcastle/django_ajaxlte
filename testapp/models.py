from django.db import models
from ajaxlte.models import BaseModel
from django.utils.html import mark_safe
from django.urls import reverse


class Foo(BaseModel):
    code = models.CharField(max_length=35, null=True, blank=True)
    name = models.CharField(max_length=165, null=True, blank=True)

    def __str__(self):
        return self.code


class Bar(BaseModel):
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=35, null=True, blank=True)
    name = models.CharField(max_length=165, null=True, blank=True)

    def __str__(self):
        return self.code

    @property
    def to_see(self):
        tag = '<a class="btn" href="%s#%s"><i class="fa fa-edit"></a>' % (reverse('testapp:Bar'), self.id)
        return mark_safe(tag)
