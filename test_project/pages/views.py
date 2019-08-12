from django.views.generic.detail import DetailView
from .models import Page

class PageView(DetailView):
    model = Page
    