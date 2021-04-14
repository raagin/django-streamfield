from django.urls import include, path
from django.contrib.auth.decorators import login_required

from . import views
from .base import get_streamblocks_models

admin_instance_urls = []

for model in get_streamblocks_models():
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
    path(
        'admin-instance/<model_name>/<int:pk>/delete/', 
        login_required(views.delete_instance), 
        name='admin-instance-delete'
    ),
    *admin_instance_urls
]
