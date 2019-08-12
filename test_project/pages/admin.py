from django.contrib import admin

from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass