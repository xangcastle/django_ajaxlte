from .utils import json, Codec, Filter
from django.http import HttpResponse
from django.forms import modelform_factory
from django.template.loader import render_to_string
import operator


def load_module(mod, cls):
    mod = __import__(mod, fromlist=[cls])
    return getattr(mod, cls)


def get_object(request):
    instance = Filter(app_label=request.POST.get('app_label'),
                      model_name=request.POST.get('model')
                      ).get_instance(request.POST.get('id'))
    return HttpResponse(json.dumps(instance.to_json(), cls=Codec), content_type='application/json')


def object_update(request):
    result = ""
    instance = Filter(app_label=request.POST.get('app_label'),
                      model_name=request.POST.get('model')
                      ).get_instance(request.POST.get('id'))
    data = request.POST.get('data', None)
    if data:
        for k, v in json.loads(str(data).replace("'", "\"")).items():
            setattr(instance, k, v)
        instance.save()
    return HttpResponse(json.dumps({'result': result, 'intance': instance.to_json()}, cls=Codec),
                        content_type='application/json')


def object_view(request):
    instance = Filter(app_label=request.POST.get('app_label'),
                      model_name=request.POST.get('model')
                      ).get_instance(request.POST.get('id'))
    try:
        result = getattr(instance, request.POST.get('view'))(request)
    except:
        result = getattr(instance, request.POST.get('view'))()
    return HttpResponse(result)


def object_execute(request):
    instance = None
    f = Filter(app_label=request.POST.get('app_label'),
                      model_name=request.POST.get('model')
                      )
    id = request.POST.get('id')
    if id:
        instance = f.get_instance(id)
    else:
        instance = f.model
    try:
        result = getattr(instance, request.POST.get('view'))(request)
    except:
        try:
            result = getattr(instance, request.POST.get('view'))()
        except:
            result = str(getattr(instance, request.POST.get('view')))
    return HttpResponse(json.dumps(result, cls=Codec), content_type='application/json')


def get_collection(request):
    queryset = Filter(app_label=request.POST.get('app_label', request.GET.get('app_label')),
                      model_name=request.POST.get('model', request.GET.get('model'))
                      ).filter_by_json(request.POST.get('filters', request.GET.get('filters')))
    return HttpResponse(json.dumps([x.to_json() for x in queryset], cls=Codec),
                        content_type='application/json')


def get_datatables(request):
    queryset = Filter(app_label=request.POST.get('app_label', request.GET.get('app_label')),
                      model_name=request.POST.get('model', request.GET.get('model'))
                      ).filter_by_json(request.POST.get('filters', request.GET.get('filters')))
    return HttpResponse(json.dumps({'data': [x.to_json() for x in queryset]}, cls=Codec),
                        content_type='application/json')


def autocomplete(request):
    result = []
    columns = request.GET.get('column_name').split(",")
    value = request.GET.get('column_value')
    columns = [('{}__like'.format(column), request.GET.get('term')) for column in columns]
    filters = request.GET.get('filters', [])
    if filters:
        filters = filters.split(",")
        filters = [tuple(x.split("=")) for x in filters]
    queryset = Filter(app_label=request.GET.get('app_label'),
                      model_name=request.GET.get('model')
                      ).filter_by_list(columns, operator.or_, filters)
    for q in queryset:
        result.append({'obj': q.to_json(),
                       'label': str(q),
                       'value': q.to_json()[value]})
    return HttpResponse(json.dumps(result, cls=Codec), content_type="application/json")


def get_html_form(request):
    resp = {}
    if request.method == "GET":
        data = {"method": "POST"}
        filter = Filter(app_label=request.GET.get('app_label'),
                        model_name=request.GET.get('model'))
        data['fields'] = request.GET.get('fields')
        data['callback'] = str(request.GET.get('callback', ""))
        data['params'] = str(request.GET.get('params', ""))
        actions = request.GET.get('action')
        _form = request.GET.get('form')
        if actions:
            data['action'] = actions
        else:
            data['action'] = '/admin/ajax/get_html_form/'
        data['app_label'] = filter.app_label
        data['model'] = filter.model_name
        id = request.GET.get('id', None)
        if _form:
            form = load_module(_form.split("-")[0], _form.split("-")[1])
        else:
            form = modelform_factory(filter.model, fields=data['fields'].split("-"))
        if id:
            form = form(instance=filter.get_instance(id))
            data['id'] = id
        else:
            form = form()
        data['form'] = form
        return HttpResponse(render_to_string("ajax/form.html", data, request))
    if request.method == "POST":
        filter = Filter(app_label=request.POST.get('app_label'),
                        model_name=request.POST.get('model'))
        form = modelform_factory(filter.model, fields=request.POST.get('fields').split("-"))
        id = request.POST.get('id', None)
        if id:
            form = form(request.POST, request.FILES or None, instance=filter.get_instance(id))
        else:
            form = form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            resp = {"result": "actualizado", "object": obj.to_json()}
        else:
            err = ""
            for e in form.errors:
                err += "error en el campo " + str(e)
            resp = {'error': err}
    return HttpResponse(json.dumps(resp, cls=Codec), content_type="application/json")
