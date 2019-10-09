from django import template
from django.utils.text import (
    get_valid_filename, 
    camel_case_to_spaces
    )
from django.utils.safestring import mark_safe
from django.template import loader

register = template.Library()


@register.simple_tag
def format_field(field):
    widget_name = get_widget_name(field)

    t = loader.select_template([
            'streamblocks/admin/fields/%s.html' % widget_name,
            'streamfield/admin/fields/%s.html' % widget_name,
            'streamfield/admin/fields/default.html'
        ])

    if widget_name == 'select':
        
        # ForeignKey Field
        if hasattr(field.field, '_queryset'):
            for obj in field.field._queryset:
                if obj.pk == field.value():
                    field.obj = obj

        # CharField choices
        if hasattr(field.field, '_choices'):
            for obj in field.field._choices:
                if obj[0] == field.value():
                    field.obj = obj[1]
        

    return mark_safe(t.render(dict(
        field=field
        )))

def get_widget_name(field):
    return get_valid_filename(
                camel_case_to_spaces(field.field.widget.__class__.__name__)
                )

@register.simple_tag
def stream_render(stream_obj, **kwargs):
    return stream_obj._render(kwargs)