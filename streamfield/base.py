import json
from django.utils.functional import cached_property
from django.utils.html import format_html_join
from django.template import loader
from django.utils.safestring import mark_safe
from django.conf import settings
from importlib import import_module

from .forms import get_form_class

__all__ = (
    'StreamObject'
)

class StreamObject:
    """
    The instance contains raw data from db and rendered html
    
    # Example: 
    # streamblocks/models.py
    
    # one value per model
    class RichText(models.Model):
        text = models.TextField(blank=True, null=True, verbose_name='Текстовое поле')   
    
    # list of values per model
    class NumberInText(models.Model):
        big_number = models.CharField(max_length=32)
        small = models.CharField(max_length=32, null=True, blank=True)
        text = models.TextField(null=True, blank=True)
        
        as_list = True

    
    # data in db
    value = [
        {
            "unique_id": "lsupu",
            "model_name": "NumberInText",
            "id": [1,2,3],
            "options":{"margins":true}
        },
        {
            "unique_id": "vlbh7j",
            "model_name": "RichText",
            "id": 1,
            "options": {"margins":true}
        }
    ]
    """

    def __init__(self, value, model_list):
        self.value = value
        self.model_list = model_list
        self.model_list_names = [m.__name__ for m in model_list]

    def __str__(self):
        return self.value or "[]"

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self or "None")

    def _iterate_over_models(self, callback, tmpl_ctx=None):
        # iterate over models and apply callback function
        data = []
        for m in self.from_json():
            model_str = m['model_name']

            if model_str in self.model_list_names:
                idx = self.model_list_names.index(model_str)
                model_class = self.model_list[idx]
                as_list = hasattr(model_class, 'as_list') and model_class.as_list
                content = {}

                # if block is not abstract model and have content in database
                if not model_class._meta.abstract:
                    if as_list:
                        unordered_items = model_class.objects.filter(pk__in=m['id'])
                        # set id as key and reorder queryset same as ids order
                        unordered_items_dict = {i.id: i for i in unordered_items}
                        content = [unordered_items_dict[i] for i in m['id']]
                    elif m['id'] != -1:
                        content = model_class.objects.get(pk=m['id'])

                ctx = dict(
                    block_model=model_str.lower(),
                    block_unique_id=m['unique_id'],
                    block_content=content,
                    as_list=as_list,
                    options=m['options']
                )

                # add tmpl_ctx if exists. tmpl_ctx: additional context from templates
                if tmpl_ctx:
                    ctx.update(tmpl_ctx)
                res = callback(model_class, model_str, content, ctx)
                data.append(res)

        return data

    def _render(self, tmpl_ctx=None):
        data = self._iterate_over_models(_get_render_data, tmpl_ctx)
        return mark_safe("".join(data))

    @cached_property
    def render(self):
        return self._render()

    def as_list(self):
        return self._iterate_over_models(_get_data_list)

    # only for complex blocks
    def render_admin(self):
        data = self._iterate_over_models(_get_render_admin_data)
        return mark_safe("".join(data))

    def from_json(self):
        return json.loads(self.value)

    @cached_property
    def to_json(self):
        return json.dumps(self.value)

def _get_block_tmpl(model_class, model_str):
    if hasattr(model_class, 'block_template'):
        return model_class.block_template
    else:
        return 'streamblocks/%s.html' % model_str.lower()


def _get_render_data(model_class, model_str, content, ctx):
    block_tmpl = _get_block_tmpl(model_class, model_str)
    try:
        t = loader.get_template(block_tmpl)
    except loader.TemplateDoesNotExist:
        ctx.update(dict(
            block_tmpl=block_tmpl,
            model_str=model_str
            ))
        t = loader.get_template('streamfield/default_block_tmpl.html')
    return t.render(ctx)

# only for complex blocks
def _get_render_admin_data(model_class, model_str, content, ctx):
    t = loader.select_template([
        'streamblocks/admin/%s.html' % model_str.lower(),
        'streamfield/admin/change_form_render_template.html'
        ])
    objs = content if isinstance(content, list) else [content]
    return format_html_join(
            '\n', "{}",
            (
                (t.render({
                    'form': get_form_class(model_class)(instance=obj)
                    }),
            ) for obj in objs)
        )

def _get_data_list(model_class, model_str, content, ctx):
    return {
        'data': ctx,
        'template': _get_block_tmpl(model_class, model_str)
        }

def get_streamblocks_models():
    streamblock_models = []

    for app in settings.INSTALLED_APPS:
        try:
            module = import_module("%s.models" % app)

            if hasattr(module, 'STREAMBLOCKS_MODELS'):
                streamblock_models.extend(module.STREAMBLOCKS_MODELS)
        except ModuleNotFoundError as e:
            pass

    return streamblock_models
