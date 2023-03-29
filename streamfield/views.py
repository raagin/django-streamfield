# -*- coding: utf-8 -*-
from django.apps import apps
from django.template import loader
from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView
from django.views.generic.detail import BaseDetailView
from .forms import get_form_class

def admin_instance(model):
    def instance_view(request, pk):
        tmpls = [
                'streamblocks/admin/%s.html' % model.__name__.lower(),
                'streamfield/admin/change_form_render_template.html'
            ]
        tmpl = getattr(model, 'custom_admin_template', loader.select_template(tmpls))
        obj = model.objects.get(pk=pk)
        ctx = {
            'form': get_form_class(model)(instance=obj),
            'object': obj
        }
        return JsonResponse({
                'content': tmpl.render(ctx),
                'title': str(obj)
                })
    return instance_view


def abstract_block_class(model, base=TemplateView):
    
    if hasattr(model, 'custom_admin_template'):
        tmpl_name = model.custom_admin_template
    else:
        tmpl = loader.select_template([
            'streamblocks/admin/%s.html' % model.__name__.lower(),
            'streamfield/admin/abstract_block_template.html'
        ])
        tmpl_name = tmpl.template.name

    attrs = dict(
        model = model,
        template_name = tmpl_name,
        )

    return type(str(model.__name__ + 'TemplateView'), (base, ), attrs )


def delete_instance(request, model_name, pk):
    model_class = apps.get_model(app_label='streamblocks', model_name=model_name)
    obj = model_class.objects.get(pk=pk)
    if request.method == 'DELETE':
        obj.delete()
        resp = {'success': True}
    else:
        resp = {'success': False}
    return JsonResponse(resp)