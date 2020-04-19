# -*- coding:utf-8 -*-
from django.db.models import Model
from django.forms.models import model_to_dict


class BaseModel(Model):

    def __iter__(self):
        for field_name in self._meta.fields():
            try:
                value = getattr(self, field_name)
            except:
                value = None
            yield (field_name, value)

    def __getitem__(self, fieldname):
        try:
            return getattr(self, fieldname)
        except:
            return None

    def __setitem__(self, fieldname, value):
        try:
            return setattr(self, fieldname, value)
        except:
            return None

    def __str__(self):
        if self.pk:
            return self._meta.verbose_name + "(%s)" % str(self.pk)
        else:
            return self._meta.verbose_name

    def to_json(self):
        o = model_to_dict(self)
        o['str'] = self.__str__()
        o['app_label'] = self._meta.app_label
        o['model'] = self._meta.object_name.lower()
        return o

    class Meta:
        abstract = True