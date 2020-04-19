from django import template
from django import forms
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="datatables_label")
def datatables_label(form, fieldname):
    return form[fieldname].label


@register.filter(name="datatables_field")
def datatables_field(form, fieldname):
    return form[fieldname]


@register.filter
def is_date(field):
    return isinstance(field.field.widget, forms.DateField)


@register.filter(name='as_inline_field')
def as_inline_field(field):
    if not isinstance(field, forms.BoundField) and settings.DEBUG:
        raise Exception('|as_inline_field got passed an invalid or inexistent field')

    attributes = {
        'field': field,
    }

    template_path = 'adminlte/datatables-field.html'
    template = get_template(template_path)

    c = Context(attributes).flatten()
    return template.render(c)


@register.filter(name="datatables_column")
def datatables_column(form, column):
    if isinstance(column, tuple):
        column_group = (column[0], column[1], 'false')
    else:
        name = column.split('.')[0]
        field = form[name]
        column_group = (field.label, column, 'true')

    return mark_safe('{title: "%s", data: "%s", orderable: %s},' % column_group)