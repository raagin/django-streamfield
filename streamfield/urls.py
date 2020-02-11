from importlib import import_module
from django.urls import include, path
from django.conf import settings
from django.contrib.auth.decorators import login_required

from . import views

STREAMBLOCKS_APP_PATH = getattr(settings, "STREAMFIELD_STREAMBLOCKS_APP_PATH", "streamblocks")
try:
    streamblocks_app = import_module("%s.models" % STREAMBLOCKS_APP_PATH)
    STREAMBLOCKS_MODELS = streamblocks_app.STREAMBLOCKS_MODELS
except (AttributeError, ValueError) as e:
    raise Exception("""Can't find STREAMBLOCKS_MODELS: wrong "STREAMFIELD_STREAMBLOCKS_APP_PATH" or STREAMBLOCKS_MODELS don't exist.""")

admin_instance_urls = []

for model in STREAMBLOCKS_MODELS:
    if not model._meta.abstract:
        block_path = path(
                    'admin-instance/%s/<int:pk>' % model.__name__.lower(), 
                    login_required(views.admin_instance_class(model).as_view()),
                    name='admin-instance'
                    )
    else:
        block_path = path(
                    'abstract-block/%s/' % model.__name__.lower(), 
                    login_required(views.abstract_block_class(model).as_view()),
                    name='abstract-block'
                    )
        
    admin_instance_urls.append(block_path)

urlpatterns = [
    *admin_instance_urls
]
