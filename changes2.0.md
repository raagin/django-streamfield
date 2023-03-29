# django-streamfield. Changes 2.0
## Major changes
1. Removed string escaping in the database. Now StreamField is stored in the database as a native JSON, since version 3.1 Django supports JSON in all databases. When resaving the object, escaping in the new version will be automatically removed.
2. New frontend features are added: You can open/collapse blocks by one or all together. You can add new block between the others blocks.
3. For better blocks navigation you can add name of the block by using __str__ method in block definition code.
4. STREAMFIELD_SHOW_ADMIN_HELP_TEXT now is False by default. And you can add your own text by using STREAMFIELD_ADMIN_HELP_TEXT in settings.
5. For development. Webpack 5 is used to build frontend part. JS scripts is divided into components. SASS is used for styling. 
6. JS libraries are join to one bundle including streamfield.
7. Removed STREAMFIELD_SHOW_ADMIN_COLLAPSE from settings.

## Minor changes
1. StreamBlocksAdminMixin now using for StreamBlocksAdmin class (#21)
2. Icons changed from png to svg
3. STREAMFIELD_SHOW_ADMIN_HELP_TEXT bug fixed (#27)
