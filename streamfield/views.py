# -*- coding: utf-8 -*-
from django.template import loader
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, TemplateView
from .forms import get_form_class

def admin_instance_class(model, base=DetailView):
    
    if hasattr(model, 'custom_admin_template'):
        tmpl_name = model.custom_admin_template
    else:
        tmpl = loader.select_template([
            'streamblocks/admin/%s.html' % model.__name__.lower(),
            'streamfield/admin/change_form_render_template.html'
        ])
        tmpl_name = tmpl.template.name
        
    def get_context_data(self, **kwargs):
        context = base.get_context_data(self, **kwargs)
        
        # forms
        obj = super(self.__class__, self).get_object()
        context['form'] = get_form_class(model)(instance=obj)

        return context

    attrs = dict(
        model = model,
        template_name = tmpl_name,
        get_context_data = get_context_data
        )

    return type(str(model.__name__ + 'DetailView'), (base, ), attrs )


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
    t = ContentType.objects.get(app_label='streamblocks', model=model_name)
    obj = t.get_object_for_this_type(pk=pk)
    if request.method == 'DELETE':
        obj.delete()
        resp = {'success': True}
    else:
        resp = {'success': False}
    return JsonResponse(resp)