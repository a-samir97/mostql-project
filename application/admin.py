from django.contrib import admin

from .models import UserStatus, UserIP, LoginDates, VisitDates, Status

admin.site.register(UserIP)
admin.site.register(UserStatus)
admin.site.register(LoginDates)
admin.site.register(VisitDates)
admin.site.register(Status)