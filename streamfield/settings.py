from django.conf import settings
from django.urls import reverse_lazy

BLOCK_OPTIONS = getattr(settings, "STREAMFIELD_BLOCK_OPTIONS", {})
SHOW_ADMIN_HELP_TEXT = getattr(settings, "STREAMFIELD_SHOW_ADMIN_HELP_TEXT", True)
DELETE_BLOCKS_FROM_DB = getattr(settings, "STREAMFIELD_DELETE_BLOCKS_FROM_DB", True)
BASE_ADMIN_URL = getattr(settings, "STREAMFIELD_BASE_ADMIN_URL", reverse_lazy('admin:index'))
