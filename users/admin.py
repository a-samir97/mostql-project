from django.contrib import admin
from .models import AppUser, AdminUser

admin.site.register(AppUser)
admin.site.register(AdminUser)
