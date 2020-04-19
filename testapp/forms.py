from django import forms
from .models import *
from ajaxlte.widgets import *


class FooForm(forms.ModelForm):
    bars = forms.Field(label="", required=False, widget=TableBordered(
        attrs={
            'columns': (
                ('code', 'Name'),
                ('name', 'Name'),
                ('to_see', ''),
            )
        }
    ))

    class Meta:
        model = Foo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs.update(initial={
                'bars': Bar.objects.filter(foo=instance)
            })
        super().__init__(*args, **kwargs)
