import json
from copy import deepcopy
from django.db import models
from django.forms.widgets import Widget
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
from .base import StreamObject
from .settings import (
    BLOCK_OPTIONS, 
    SHOW_ADMIN_HELP_TEXT, 
    DELETE_BLOCKS_FROM_DB, 
    BASE_ADMIN_URL
    )


class StreamFieldWidget(Widget):
    template_name = 'streamfield/streamfield_widget.html'

    def __init__(self, attrs=None):
        self.model_list = attrs.pop('model_list', [])
        
        model_list_info = {}
        for block in self.model_list:
            as_list = hasattr(block, "as_list") and block.as_list
        
            options = block.options if hasattr(block, "options") else BLOCK_OPTIONS
            if hasattr(block, "extra_options"):
                options = deepcopy(options)
                options.update(block.extra_options)

            model_doc = block._meta.verbose_name_plural if as_list else block._meta.verbose_name
            model_list_info[block.__name__] = {
                'model_doc': str(model_doc),
                'abstract': block._meta.abstract,
                'as_list': as_list,
                'options': options
            }
        
        attrs["model_list_info"] = json.dumps(model_list_info)
        attrs['show_admin_help_text'] = SHOW_ADMIN_HELP_TEXT
        attrs['delete_blocks_from_db'] = DELETE_BLOCKS_FROM_DB
        attrs['base_admin_url'] = BASE_ADMIN_URL
        super().__init__(attrs)

    def format_value(self, value):
        if value != "" and not isinstance(value, StreamObject):
            value = StreamObject(value, self.model_list)            
        return value

    class Media:
        css = {
            'all': ('streamfield/css/streamfield_widget.css',)
        }
        js = (
            'streamfield/vendor/lodash.min.js',
            'streamfield/vendor/js.cookie.js',
            'streamfield/vendor/vue.min.js',
            'streamfield/vendor/Sortable.min.js',
            'streamfield/vendor/vuedraggable.umd.min.js',
            'streamfield/vendor/axios.min.js',
            'streamfield/js/streamfield_widget.js',
            )

class StreamField(models.TextField):
    description = "StreamField"

    def __init__(self, *args, **kwargs):
        self.model_list = kwargs.pop('model_list', [])
        self.popup_size = kwargs.pop('popup_size', (1000, 500))
        kwargs['blank'] = True
        kwargs['default'] = "[]"
        super().__init__(*args, **kwargs)


    def from_db_value(self, value, expression, connection):
        return self.to_python(json.loads(value))
        
    def to_python(self, value):
        if not value or isinstance(value, StreamObject):
            return value
        return StreamObject(value, self.model_list)

    def get_prep_value(self, value):
        return json.dumps(str(value))

    def formfield(self, **kwargs):
        widget_class = kwargs.get('widget', StreamFieldWidget)
        attrs = {}
        attrs["model_list"] = self.model_list
        attrs["data-popup_size"] = list(self.popup_size)
        defaults = {
            'widget': widget_class(attrs=attrs),
        }
        return super().formfield(**defaults)


FORMFIELD_FOR_DBFIELD_DEFAULTS[StreamField] = {'widget': StreamFieldWidget}
