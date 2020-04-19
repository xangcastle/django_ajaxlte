# -*- coding:utf-8 -*-


def menu(request):
    return {
        'menu':
            {
                'pills': [
                    {
                        'name': "Test",
                        'links': [
                            {'name': 'test', 'url': ''},
                            {'name': 'test', 'url': '',
                             'has_treeview': True, 'tree': [
                                {'name': 'test', 'url': ''},
                            ]},
                        ]
                    },
                ]
            }
    }
