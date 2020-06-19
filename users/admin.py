from django.contrib import admin
from .models import AppUser, AdminUser, Accounts

admin.site.register(AppUser)
admin.site.register(AdminUser)
admin.site.register(Accounts)