# Django StreamField

This is a simple realisation of StreamField's idea of Wagtail CMS for plain Django admin or with Grappelli skin.

## Highlights
You can build your page with different kind of blocks. 
Sort them and sort the lists inside the blocks.

**The blocks here are regular instances of Django models.** For editing content inside the blocks, it use native popup mechanism in Django admin interface.
This allow you to use other field's widgets inside the blocks as is.
For example, if you want to use in your blocks FileBrowseField
from django-filebrowser, it will perfectly working 
without any additional settings.

Module also working with [Grappelli Interface](https://github.com/sehmaschine/django-grappelli) (Optional)

![django-streamfield demo screenshot](https://raagin.ru/assets/uploads/django-streamfield.png)

## Contents

- [Installation](#installation)
- [How to use](#how-to-use)
- [Admin](#admin)
  - [Custom admin class for block's models](#custom-admin-class-for-blocks-models)
  - [Custom templates for render block models in admin](#custom-templates-for-render-block-models-in-admin)
  - [Override how to render block's fields in admin](#override-how-to-render-blocks-fields-in-admin)
  - [Override list of blocks for your StreamField in admin.py](#override-list-of-blocks-for-your-streamfield-in-adminpy)
- [Block options](#block-options)
- [Special cases](#special-cases)
  - [Complex Blocks](#complex-blocks)    
  - [Blocks without data in database. Only templates](#blocks-without-data-in-database-only-templates)
  - [Add extra context to blocks](#add-extra-context-to-blocks)
  - [Get field data as list](#get-field-data-as-list)
  - [Cache for reduce the number of database requests](#cache-for-reduce-the-number-of-database-requests)
- [Settings](#settings)

## Installation

Requirements: `django>=2.*`

`pip install django-streamfield`

## How to use
- Create streamblocks app with your models
- Add streamfield and streamblocks to INSTALLED_APPS
- Add streamfield.urls
- Create templates for streamblocks
- Add StreamField to your model
- Use it in templates

**1. Create new app called `streamblocks` and put there some models**

...that you want to use as blocks in your StreamField.  
Add them to the list `STREAMBLOCKS_MODELS`.
For example:

```python
# streamblocks/models.py

# one object
class RichText(models.Model):
    text = models.TextField(blank=True, null=True)   

    class Meta:
        # This will use as name of block in admin
        verbose_name="Text"

# list of objects
class ImageWithText(models.Model):
    image = models.ImageField(upload_to="folder/")
    text = models.TextField(null=True, blank=True)
    
    # StreamField option for list of objects
    as_list = True

    class Meta:
        verbose_name="Image with text"
        verbose_name_plural="Images with text"

# Register blocks for StreamField as list of models
STREAMBLOCKS_MODELS = [
    RichText,
    ImageWithText
]
```
> Important!: Don't use 'as_list', 'options', 'extra_options' as models field names, because they are used by streamfield.

**2. Add apps to settings.py and make migrations**

Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'streamblocks',
    'streamfield',
    ...
```
Run `python manage.py makemigrations` and `python manage.py migrate`

**3. Add streamfield.urls to main urls.py**
```python
urlpatterns += [
    path('streamfield/', include('streamfield.urls'))
]
```

**4. Create templates for each block model, named as lowercase names of the models:**

1. streamblocks/templates/streamblocks/richtext.html
2. streamblocks/templates/streamblocks/imagewithtext.html

And use `block_content` as context.

> Note: block_content will be single object 
if no 'as_list' property in your model, 
and will be a list of objects if there is.

```html
<!--richtext.html-->
<div class="rich-text-block">
    {{ block_content.text|safe }}
</div>
```
```html
<!--imagewithtext.html-->
<ul class="image-with-text-block">
    {% for block in block_content %}
    <li>
        <img src="{{ block.image.url }}" alt="">
        <p>{{ block.text }}</p>
    </li>
    {% endfor %}
</ul>
```

> Note: You may use also `block_template` option. For specify a block template file.

```python
class RichText(models.Model):
    ...
    block_template = "streamblocks/richtext.html"
    ...
```
> Note: If you need unique string in block template, use `block_model` and `block_unique_id`

*Full list of variables in template context:*  
- `block_model` (lowercase of modelname - "richtext")
- `block_unique_id` (unique string)
- `block_content` (block data from db)
- `as_list` (boolean)
- `options` ([block options](#block-options))

> Note: For unique idetifier inside the lists you may use a combination of `block_unique_id` and `block.id` of subblock.

**5. Add StreamField to your model in your application**

And add the models that you want to use in this stream as model_list
```python
# models.py
from streamfield.fields import StreamField
from streamblocks.models import RichText, ImageWithText

class Page(models.Model):
    stream = StreamField(
        model_list=[ 
            RichText,
            ImageWithText
        ],
        verbose_name="Page blocks"
        )
```

*You can set size of popup window*  
Add `popup_size` attribute to StreamField
```python
    ...
    stream = StreamField(
        model_list=[...],
        popup_size=(1000, 500) # default value. Width: 1000px, Height: 500px
        )
    ...
```

**6. Use it in template**
If you have your `page` in context, 
you can get content by field's cached property page.stream.render
```html
...
<div class="content">
    {{ page.stream.render }}
</div>
...
```

Or, if you need extra context in blocks, you may use template tag:
```html
{% load streamfield_tags %}
...
<div class="content">
  {% stream_render page.stream request=request %}
</div>
...
```
Third way it's to use list. [See bellow](#get-field-data-as-list)


## Admin
### Custom admin class for block's models
Models will automaticaly register in admin.
If you want provide custom admin class, 
first unregister models and register again, using `StreamBlocksAdmin` class.

```python
# streamblocks/admin.py

from django.contrib import admin
from streamfield.admin import StreamBlocksAdmin

from streamblocks.models import RichText

admin.site.unregister(RichText)
@admin.register(RichText)
class RichTextBlockAdmin(StreamBlocksAdmin, admin.ModelAdmin):
    pass
```

### Custom templates for render block models in admin
If you need to customize admin templates for block models wich you are using, you need to put templates named as 
described in section 3 (above). but put it inside "admin" folder.

For example for RichText block it will be:

`streamblocks/templates/streamblocks/admin/richtext.html`

As context use "form" and/or "object":
```html
{{ form.text.value }}
{{ object }}
```

The default admin template is: `streamfield/admin/change_form_render_template.html`  
You can extend it
```html
{% extends "streamfield/admin/change_form_render_template.html" %}
{% block streamblock_form %}
{{ block.super }}
Original object is: {{ object }}
{% endblock streamblock_form %}
```


You may also specify custom template as option:
```python
class RichText(models.Model):
    ...
    custom_admin_template = "streamblocks/admin/richtext.html"
    ...
```

### Override how to render block's fields in admin
Create custom template for field with name as generated by `django.utils.text.camel_case_to_spaces` from field widget name, and put it inside `.../streamblocks/admin/fields/` folder.

For example for TextField widget (Textarea) of RichText block, it will be:
`streamblocks/templates/streamblocks/admin/fields/textarea.html`

And `MyCustomWidget`:
`streamblocks/templates/streamblocks/admin/fields/my_custom_widget.html`

As context use "field":
```html
{{ field.value|default:""|safe }}
```

### Override list of blocks for your StreamField in admin.py
Typicaly you set the blocks in your models as `model_list` attribute of StreamField field.
But if you want to change blocks, for example depending on object, you can do it in admin site
of your model. Suppose you want to use only `RichText` on page with id=1.

```python
# admin.py
from streamfield.fields import StreamFieldWidget
from streamblocks.models import RichText
from .models import Page

@admin.register(Page)
class PageAdmin(models.Admin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.id == 1:
            form.base_fields['stream'].widget = StreamFieldWidget(attrs={
                'model_list': [ RichText ]
                })
        return form
```
Be careful with already existing blocks in db. If you remove them from admin, it produce error.

## Block options
You may use `options` property in your streamblocks models to add some additional options to your block.
This is useful with `as_list` property when you need to add some options to whole block not separatly to each object of this list.

For example:
```python
# streamblocks/models.py

# list of objects as slider
class Slide(models.Model):
    image = models.ImageField(upload_to="folder/")
    text = models.TextField(null=True, blank=True)
    
    # StreamField option for list of objects
    as_list = True
    
    options = {
        'autoplay': {
            'label': 'Autoplay slider',
            'type': 'checkbox',
            'default': False
        },
        'width': {
            'label': 'Slider size',
            'type': 'select',
            'default': 'wide',
            'options': [
                {'value': 'wide', 'name': 'Wide slider'},
                {'value': 'narrow', 'name': 'Narrow slider'},
            ]
        },
        'class_name': {
          'label': 'Class Name',
          'type': 'text',
          'default': ''
        }
    }

    class Meta:
        verbose_name="Slide"
        verbose_name_plural="Slider"
```
In block template you can use this options as `options.autoplay`
In page admin you will see it on the bottom of this block.
> Note: Now only "checkbox", "text" and "select" type is working.
You may apply options for all blocks with `STREAMFIELD_BLOCK_OPTIONS` (See [Settings](#settings))

If you want to add block options to options, which was set in django settings, you may use `extra_options`.
```python
class Slide(models.Model):
    ...
    extra_options = {
        "autoplay": {
            "label": "Autoplay",
            "type": "checkbox",
            "default": False
        }
    }
    ...
```

If you want to switch off options, which set in django settings, for current block. Set `options={}`

## Special cases
### Complex Blocks
You may use StreamField as part of blocks and create with that way complex structure
and use `{{ block_content.<field_name>.render }}`

### Blocks without data in database. Only templates.
You may use it for widgets or separators or for whatever you want...
Just make the block model `abstract`.
```python
class EmptyBlock(models.Model):
    class Meta:
        abstract = True
        verbose_name='Empty space'
```
and use `streamblocks/templates/streamblocks/emptyblock.html` for your content.
> Note: Don't forget to register a block in STREAMBLOCKS_MODELS

### Add extra context to blocks
Supose, you need to add some data to blocks from global context.
Instead of using render property in template `{{ page.stream.render }}`,
you need to use template tag `stream_render` from `streamfield_tags` with keywords arguments.

For example, if you have in page template `request` and `page` objects and want to use it in blocks:
```html
{% load streamfield_tags %}
...
<div class="content">
  {% stream_render page.stream request=request page=page %}
</div>
...
```

### Get field data as list
If you have special case, you can get data as list.

```python
# views.py
stream_list = page.stream.as_list()
# You will get list of dictionaries 
# print(stream_list)
[{
    'data': {
        'block_model': '.....', 
        'block_unique_id': '....', 
        'block_content': [...], 
        'as_list': True, 
        'options': {}
    }, 
    'template': '....'
    },
    ...
]
```

```html
<!-- template.html -->
{% for b in page.stream.as_list %}
    {% include b.template with block_content=b.data.block_content %}
{% endfor %}
```



### Cache for reduce the number of database requests
There is two ways of caching:
- Simple cache view with django cache 
- Create additional field, for example: 'stream_rendered'
and render to this field html in save method

```python
def save(self, *args, **kwargs):
    self.stream_rendered = self.stream.render
    super().save(*args, **kwargs)
```
...and use this field in your html

## Settings
```python
# settings.py
```

### STREAMFIELD_SHOW_ADMIN_HELP_TEXT
If you want to hide "Help" link in admin, above the "Add new block" link.
Set: 
```python
STREAMFIELD_SHOW_ADMIN_HELP_TEXT = False
```

### STREAMFIELD_DELETE_BLOCKS_FROM_DB
If you want to keep streamblock's instances in db, when you removing it from StreamField. Set: 
```python
STREAMFIELD_DELETE_BLOCKS_FROM_DB = False
```
It was default behavior in previous releases. 
> Note: If you delete entire object which contain StreamField, streamblock's instances will not be deleted. You should care about it by yourself.

### STREAMFIELD_BLOCK_OPTIONS

You may use `STREAMFIELD_BLOCK_OPTIONS` in settings.py to add some options to all blocks.

For example:
```python
STREAMFIELD_BLOCK_OPTIONS = {
    "margins": {
        "label": "Margins",
        "type": "checkbox",
        "default": True
    }
}
```
In block template use `{{ options.margins }}`

> Note: Now only "checkbox", "text",  and "select" type is working.

