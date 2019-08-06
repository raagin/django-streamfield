# Django StreamField

This is a simple realisation of StreamField's idea 
from [Wagtail CMS](https://wagtail.io)  

## Highlights
You can build your page with different kind of blocks. 
Sort them and sort the lists inside the blocks.

For editing content inside the blocks, it use native popup mechanism in Django admin interface.
This allow you to use other field's widgets inside the blocks as is.
For example, if you want to use in your blocks FileBrowseField
from django-filebrowser, it will perfectly working 
without any additional settings.

Module also working with [Grappelli Interface](https://github.com/sehmaschine/django-grappelli) (Optional)


## Installation
`pip install django-streamfield`

## How to use

**1. Create new app called `streamblocks`**

**2. Put to `streamblocks/models.py` some models**

...that you want to use in your stream field.
And add this models in STREAMBLOCKS_MODELS list.
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

# Register blocks for StreamField as list of models
STREAMBLOCKS_MODELS = [
    RichText,
    ImageWithText
]
```

**3. Create templates for each models above, named as lowercase names of the models:**

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

**4. Add apps to settings.py**

Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'streamblocks',
    'streamfield',
    ...
```

**5. Add streamfield.urls to main urls.py**
```python
urlpatterns += [
    path('streamfield/', include('streamfield.urls'))
]
```

**6. Add StreamField to your model in your application**

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

Then if you have your 'page' in context, 
you can get content by field cached property page.stream.render
```html
...
<div class="content">
    {{ page.stream.render }}
</div>
...
```


## Custom Admin for block's models
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
If you need to customize admin templates of the fields wich you are using, you need to put templates named as 
described in section 3 (above). but put it inside "admin" folder.
For example for RichText block it will be:

streamblocks/templates/streamblocks/admin/richtext.html

As context use "form":
```html
{{ form.text.value }}
```

## Complex Blocks
You may use StreamField as part of blocks and create with that way complex structure
and use `{{ block_content.<field_name>.render }}`

## Blocks without data in database. Only templates.
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

## Cache for reduce the number of database requests
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
**STREAMFIELD_STREAMBLOCKS_APP_PATH**

If your app `streamblocks` located not in project root directory, you need to reflect it in settings.py
```python
STREAMFIELD_STREAMBLOCKS_APP_PATH = 'yourapps.streamblocks'
```

**STREAMFIELD_BLOCK_OPTIONS**

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
In template use `{{ options.margins }}`

> Note: Now only type "checkbox" is working, the other options in plan.

