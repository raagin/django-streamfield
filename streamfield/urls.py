from django.urls import include, path

from . import views
from .settings import STREAMBLOCKS_MODELS

admin_instance_urls = []

for model in STREAMBLOCKS_MODELS:
    if not model._meta.abstract:
        admin_instance_urls.append(path(
                    'admin-instance/%s/<int:pk>' % model.__name__.lower(), 
                    views.admin_instance_class(model).as_view(),
                    name='admin-instance'
                    ))

urlpatterns = [
    *admin_instance_urls
]
