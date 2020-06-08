from django.contrib import admin

from .models import Logging, Note

admin.site.register(Logging)
admin.site.register(Note)