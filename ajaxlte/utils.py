# -*- coding:utf-8 -*-
import json
from django.db.models import Q, Max
import operator
import datetime
import decimal
from functools import reduce
from django.db.models.fields.files import ImageFieldFile, FileField, FieldFile
from django.contrib.contenttypes.models import ContentType


def get_code(entity, length=4):
    model = type(entity)
    code = ''
    sets = model.objects.filter(code__isnull=False)
    if sets:
        maxi = str(sets.aggregate(Max('code'))['code__max'])
        if maxi:
            consecutive = list(range(1, int(maxi)))
            busy = list(sets.values_list('code', flat=True))
            n = 0
            for l in busy:
                busy[n] = int(str(l))
                n += 1
            available = list(set(consecutive) - set(busy))
            if len(available) > 0:
                code = min(available)
            else:
                code = max(busy) + 1
    else:
        code = 1
    return str(code).zfill(length)


def get_number(entity, length=4):
    model = type(entity)
    code = ''
    sets = model.objects.filter(number__isnull=False)
    if sets:
        maxi = str(sets.aggregate(Max('number'))['number__max'])
        if maxi:
            consecutive = list(range(1, int(maxi)))
            busy = list(sets.values_list('number', flat=True))
            n = 0
            for l in busy:
                busy[n] = int(str(l))
                n += 1
            available = list(set(consecutive) - set(busy))
            if len(available) > 0:
                code = min(available)
            else:
                code = max(busy) + 1
    else:
        code = 1
    return str(code).zfill(length)


def json_object(instance, model):
    if instance:
        return instance.to_json()
    else:
        return model().to_json()


def json_choice(choice_name, instance):
    try:
        return {'id': getattr(instance, choice_name), 'name': getattr(instance, 'get_%s_display' % choice_name)()}
    except:
        return None


class Codec(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%d/%m/Y %H:%M:%S')
        elif isinstance(obj, datetime.time):
            return obj.strftime('H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%d/%m/%Y')
        elif isinstance(obj, FieldFile):
            try:
                return obj.url
            except:
                return 'null'
        elif isinstance(obj, FileField):
            try:
                return obj.url
            except:
                return 'null'
        elif isinstance(obj, ImageFieldFile):
            try:
                return obj.url
            except:
                return 'null'
        elif obj == None:
            return 'null'
        else:
            return json.JSONEncoder.default(self, obj)


class Filter(object):
    app_label = None
    model_name = None
    model = None

    def __init__(self, app_label, model_name):
        self.app_label = app_label
        self.model_name = model_name
        self.model = ContentType.objects.get(app_label=app_label, model=model_name).model_class()

    def get_instance(self, pk):
        return self.model.objects.get(pk=pk)

    @staticmethod
    def _like(sentence, field_name, separator=" ", filters=[]):
        for word in sentence.split(separator):
            filters.append(('{}__icontains'.format(field_name.replace('__like', '')), word))
        return filters

    def format(self, filters):
        final_filter = []
        for f in filters:
            if f[0].find('__like') > -1:
                final_filter = self._like(f[1], f[0], filters=final_filter)
            else:
                final_filter.append(f)
        return [Q(x) for x in final_filter]

    def filter_by_json(self, filters=None, op=operator.and_):
        if filters:
            final_filter = []
            for k, v in json.loads(str(filters).replace("'", "\"")).items():
                final_filter.append((str(k), str(v)))
            return self.model.objects.filter(reduce(op, self.format(final_filter)))
        else:
            return self.model.objects.all()

    def filter_by_list(self, filters=[], op=operator.and_, extra=None):
        if len(filters) > 0:
            qs = self.model.objects.filter(reduce(op, self.format(filters)))
            if extra:
                qs = qs.filter(reduce(operator.and_, self.format(extra)))
            return qs
        else:
            return self.model.objects.all()
