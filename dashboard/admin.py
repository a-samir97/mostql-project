from django.contrib import admin

from .models import Logging, Note, InboxMessages, CertifiedRequest, Reports

admin.site.register(Logging)
admin.site.register(Note)
admin.site.register(InboxMessages)
admin.site.register(CertifiedRequest)
admin.site.register(Reports)
