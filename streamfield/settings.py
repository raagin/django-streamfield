from django.conf import settings
from django.urls import reverse_lazy
from django.template.loader import render_to_string

BLOCK_OPTIONS = getattr(settings, "STREAMFIELD_BLOCK_OPTIONS", {})
SHOW_ADMIN_COLLAPSE = getattr(settings, "STREAMFIELD_SHOW_ADMIN_COLLAPSE", True)
DELETE_BLOCKS_FROM_DB = getattr(settings, "STREAMFIELD_DELETE_BLOCKS_FROM_DB", True)
BASE_ADMIN_URL = getattr(settings, "STREAMFIELD_BASE_ADMIN_URL", reverse_lazy('admin:index'))
BLOCK_TITLE = getattr(settings, "STREAMFIELD_BLOCK_TITLE", '__str__')

SHOW_ADMIN_HELP_TEXT = getattr(settings, "STREAMFIELD_SHOW_ADMIN_HELP_TEXT", False)
if SHOW_ADMIN_HELP_TEXT:
	ADMIN_HELP_TEXT = getattr(settings, "STREAMFIELD_ADMIN_HELP_TEXT", render_to_string('streamfield/streamfield_admin_help.html'))
else:
	ADMIN_HELP_TEXT = ""
