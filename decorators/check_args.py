# -*- coding: utf-8 -*- #
"""
    check request args
"""
import json
from django.http import HttpResponse


__author__ = 'fashust'
__email__ = 'fashust.nefor@gmail.com'


def check_args(function=None, form_class=None, fields=None, *args, **kwargs):
    """
        check request args for ajax
        :param function
        :param form_class
        :param fields
        :param args
        :param kwargs
    """
    def _dec(view_func):
        """
            dec
            :param view_func
        """
        def _view(request, *args, **kwargs):
            """
                _view
                :param request
                :param args
                :param kwargs
            """
            status = True
            error = False
            data = {}
            if request.is_ajax():
                if form_class:
                    form = form_class(request.POST)
                    if not form.is_valid():
                        status = False
                        error = True
                        data.update({'error_fields': form.errors.keys()})
                if fields:
                    for field in fields:
                        if '[]' in field:
                            if not request.POST.getlist(field, None):
                                status = False
                                error = True
                                data.update(
                                    {'message': 'No %s in request.' % field}
                                )
                                break
                        elif not request.POST.get(field, None):
                            status = False
                            error = True
                            data.update(
                                {'message': 'No %s in request.' % field}
                            )
                            break
            else:
                status = False
                error = True
                data.update({'message': 'Method not allowed'})
            if not status:
                return HttpResponse(json.dumps({
                    'status': status,
                    'error': error,
                    'data': data
                }), mimetype='application/json', content_type='charset=utf-8')
            return view_func(request, *args, **kwargs)
        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__
        return _view
    if function:
        return _dec(function)
    return _dec
