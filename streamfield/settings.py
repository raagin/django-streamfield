from importlib import import_module

from django.conf import settings

BLOCK_OPTIONS = getattr(settings, "STREAMFIELD_BLOCK_OPTIONS", {})
SHOW_ADMIN_HELP_TEXT = getattr(settings, "STREAMFIELD_SHOW_ADMIN_HELP_TEXT", True)
DELETE_BLOCKS_FROM_DB = getattr(settings, "STREAMFIELD_DELETE_BLOCKS_FROM_DB", True)
