# Django StreamField

This is a simple realisation of StreamField's idea 
from [Wagtail CMS](https://wagtail.io) for plain Django admin 
or with Grappelli skin. 

Does not work with sqlite DB yet.

For editing content we use native popup mechanism in Django admin interface.
This allow us to use other field's widgets inside the blocks as is.

For example, if you want to use in your blocks FileBrowseField 
from django-filebrowser, it will perfectly working 
without any additional settings.

## Installation
`pip install django-streamfield`

## How to use

**Create new app called `streamblocks`**

**Put to `streamblocks/models.py` some models**

that you want to use in your stream field.
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
        verbose_name="Images with text"
```

**In `streamblocks/models.py` register blocks**

for StreamField as list of your block models
```python
# streamblocks/models.py

...

STREAMBLOCKS = [
    RichText,
    ImageWithText
]
```

**Create templates for each models above, named as lowercase names of the models:**

1. streamblocks/templates/streamblocks/richtext.html
2. streamblocks/templates/streamblocks/imagewithtext.html

And use `block_content` as context.

> Note: block_content will be single object 
if no 'as_list' property in your model, 
and will be a list of objects if there is.

```html
<!--richtext.html-->
<div class="rich-text-block">
    {{ block_content|safe }}
</div>

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

**Add apps to settings.py**

Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'streamblocks',
    'streamfield',
    ...
```

**Add streamfield.urls to main urls.py**
```python
urlpatterns += [
    path('streamfield/', include('streamfield.urls'))
]
```

**Add StreamField to your model in your application**

And add the models that you want to use in this stream as model_list
```python
# models.py
from streamfield.fields import StreamField

class Page(models.Model):
    stream = StreamField(
        model_list=[ 
            RichText,
            ImageWithText
        ],
        verbose_name="Page blocks"
        )
```

Then if you have your 'page' in context, 
you can get content by calling method page.stream.render()
```html
...
<div class="content">
    {{ page.stream.render }}
</div>
...
```


## Custom Admin for block's models
Models will automaticaly register in admin
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

## Complex Blocks
You may use StreamField as part of blocks and create with that way complex structure
and use `{{ block_content.<field_name>.render }}`

## Cache for reduce the number of database requests
There is two ways of caching:
- Simple cache view with django cache 
- Create additional field, for example: 'stream_rendered'
and render to this field html in save method

```python
def save(self, *args, **kwargs):
    self.stream_rendered = self.stream.render()
    super().save(*args, **kwargs)
```
...and use this field in your html

## Settings
You may use `STREAMFIELD_BLOCK_OPTIONS` in settings.py to add some options to block.

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
> Note: Now only type "checkbox" is working, the other options in plan.

