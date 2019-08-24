from django.contrib import admin
from streamfield.admin import StreamBlocksAdmin
from streamblocks.models import RichText, Column

class RichTextAdmin:
    # rich text admin class
    pass

admin.site.unregister(RichText)
@admin.register(RichText)
class RichTextBlockAdmin(StreamBlocksAdmin, RichTextAdmin):
    pass

admin.site.unregister(Column)
@admin.register(Column)
class ColumnBlockAdmin(StreamBlocksAdmin):
    pass

