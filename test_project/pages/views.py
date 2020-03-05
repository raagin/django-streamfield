from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Page

class PageView(DetailView):
    model = Page

def index(request):
    return render(request, 'pages/index.html', dict(pages=Page.objects.all()))
    