from importlib import import_module

from django.conf import settings

BLOCK_OPTIONS = getattr(settings, "STREAMFIELD_BLOCK_OPTIONS", {})
STREAMBLOCKS_APP_PATH = getattr(settings, "STREAMFIELD_STREAMBLOCKS_APP_PATH", "streamblocks")

try:
    streamblocks_app = import_module("%s.models" % STREAMBLOCKS_APP_PATH)
    STREAMBLOCKS_MODELS = streamblocks_app.STREAMBLOCKS_MODELS
except (AttributeError, ValueError) as e:
    raise Exception("""Can't find STREAMBLOCKS_MODELS: wrong "STREAMFIELD_STREAMBLOCKS_APP_PATH" or STREAMBLOCKS_MODELS don't exist.""")
