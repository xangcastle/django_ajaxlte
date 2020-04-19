from django import template
import re
from django.urls import reverse
from django.template.loader import render_to_string


class _Menu:
    parents = []
    children = []
    models_icon = {}

    def clear(self):
        self.parents = []
        self.children = []

    def add(self, label, link='', icon='', id_='', parent=''):

        if id_ == '':
            id_ = label

        if parent != '':
            child = {
                id_: {
                    'label': label,
                    'link': link,
                    'icon': icon,
                    'children': []
                }
            }

            self.children.append(child)

            for idx, parent_item in enumerate(self.parents):

                if parent in parent_item:
                    self.parents[idx][parent]['children'].append(child)
                else:
                    for idx, child_item in enumerate(self.children):
                        if parent in child_item:
                            self.children[idx][parent]['children'].append(child)

        else:
            self.parents.append({
                id_: {
                    'label': label,
                    'link': link,
                    'icon': icon,
                    'children': []
                }
            })

    def render(self, context, menus=None):
        context['menu'] = menus
        return render_to_string('adminlte/menu.html', context=context)

    def admin_apps(self, context, r):
        print('context', context)
        print('r', r)
        request = context['request']
        for app in context['available_apps']:
            if str(app['app_url']) in request.path:
                r += '<li class="nav-item has-treeview menu-open"><a href="#" class="nav-link active"><i class="nav-icon fas fa-edit"></i> <p>%s</p><p><i class="fas fa-angle-left right"></i></p></a><ul class="nav nav-treeview">\n' % (
                    app['name'])
            else:
                r += '<li class="nav-item has-treeview"><a href="#" class="nav-link"><i class="nav-icon fas fa-edit"></i> <p>%s</p><p><i class="fas fa-angle-left right"></i></p></a><ul class="nav nav-treeview">\n' % (
                    app['name'])

            for model in app['models']:
                if 'add_url' in model:
                    url = model['add_url']

                if 'change_url' in model:
                    url = model['change_url']

                # if 'delete_url' in model:
                #     url = model['delete_url']

                if 'admin_url' in model:
                    url = model['admin_url']

                icon = '<i class="far fa-circle nav-icon"></i>'
                if model['object_name'].title() in self.models_icon:
                    if self.models_icon[model['object_name'].title()] != '':
                        if re.match(r'\<([a-z]*)\b[^\>]*\>(.*?)\<\/\1\>',
                                    self.models_icon[model['object_name'].title()]):
                            icon = self.models_icon[model['object_name'].title()]
                        else:
                            icon = '<i class="%s"></i>' % (self.models_icon[model['object_name'].title()])
                if request.path == url:
                    r += '<li class="nav-item"><a href="%s" class="nav-link active">%s %s</a></li>' % (
                        url, icon, model['name'])
                else:
                    r += '<li class="nav-item"><a href="%s" class="nav-link">%s %s</a></li>' % (
                        url, icon, model['name'])

            r += '</ul></li>\n'

        return r

    def app_menu(self, context, r):
        print('context', context)
        print('r', r)
        return r

    def set_model_icon(self, model_name, icon):
        self.models_icon[model_name.title()] = icon

    def get_model_icon(self, context):

        icon = '<i class="far fa-circle nav-icon"></i>'
        if context['model']['object_name'].title() in self.models_icon:

            if self.models_icon[context['model']['object_name'].title()] != '':
                if re.match(r'<([a-z]*)\b[^>]*>(.*?)</\1>', self.models_icon[context['model']['object_name'].title()]):
                    icon = self.models_icon[context['model']['object_name']]
                else:
                    icon = '<i class="%s"></i>' % (self.models_icon[context['model']['object_name'].title()])

        return icon


register = template.Library()

Menu = _Menu()


@register.simple_tag(takes_context=True, name='main_menu')
def menu_tag(context):
    return Menu.admin_apps(context, Menu.render(context))


@register.simple_tag(takes_context=True, name='icon')
def icon_tag(context):
    return Menu.get_model_icon(context)
