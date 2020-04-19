# -*- coding:utf-8 -*-
from django.forms import Widget, Select


def get_all_fields_from_form(instance):
    fields = list(instance().base_fields)

    for field in list(instance().declared_fields):
        if field not in fields:
            fields.append(field)
    return fields


class SelectSearch(Select):
    template_name = "ajaxlte/widgets/select-search.html"

    def build_attrs(self, base_attrs, extra_attrs=None):
        extra_attrs.update({
            'class': "selectpicker",
            'data-live-search': "true",
        })
        return super().build_attrs(base_attrs, extra_attrs=extra_attrs)


class TableBordered(Widget):
    template_name = "ajaxlte/widgets/table-bordered.html"

    def format_value(self, value):
        return value


class TableBorderedInput(Widget):
    template_name = "ajaxlte/widgets/table-bordered-input.html"

    def format_value(self, value):
        if value:
            return [self.attrs['form'](instance=x) for x in value]
        return value

    def build_attrs(self, base_attrs, extra_attrs=None):
        updated_attrs = dict()
        updated_attrs['columns'] = get_all_fields_from_form(base_attrs['form'])
        updated_attrs['model'] = str(base_attrs['form']._meta.model.__name__).lower() + "_id"
        updated_attrs['opts'] = base_attrs['form']._meta.model._meta
        extra_attrs.update(updated_attrs)
        return super().build_attrs(base_attrs, extra_attrs)


class FormWidget(Widget):
    template_name = "ajaxlte/widgets/form-widget.html"

    def format_value(self, value):
        try:
            return self.attrs['form'](instance=self.attrs['model'].objects.get(id=value))
        except:
            return self.attrs['form']