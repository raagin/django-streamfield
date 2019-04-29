# -*- coding: utf-8 -*-
import copy

from django.views.generic import DetailView, TemplateView

from rest_framework import viewsets

from .serializers import get_serializer_class
from .forms import get_form_class

def get_viewset_class(model, base=viewsets.ModelViewSet):
    attrs = dict(
        queryset = model.objects.all(),
        serializer_class = get_serializer_class(model)
        )

    return type(str(model.__name__ + 'ViewSet'), (base, ), attrs )


def admin_instance_class(model, base=DetailView):
    tmpl = 'streamfield/admin/change_form_render_template.html'

    if hasattr(model, 'custom_admin_template'):
        tmpl = model.custom_admin_template

    def get_context_data(self, **kwargs):
        context = base.get_context_data(self, **kwargs)
        
        # forms
        obj = super(self.__class__, self).get_object()
        context['form'] = get_form_class(model)(instance=obj)

        return context

    attrs = dict(
        model = model,
        template_name = tmpl,
        get_context_data = get_context_data
        )

    return type(str(model.__name__ + 'DetailView'), (base, ), attrs )
