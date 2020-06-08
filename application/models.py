from django.db import models

from users.models import AppUser

class Accounts(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    whatsapp = models.CharField(max_length=50, null=True, blank=True)
    facebook = models.CharField(max_length=50, null=True, blank=True)
    instgram = models.CharField(max_length=50, null=True, blank=True)
    gmail = models.CharField(max_length=50, null=True, blank=True)
    youtube = models.CharField(max_length=50, null=True, blank=True)
    linkedin = models.CharField(max_length=50, null=True, blank=True)
    twitter = models.CharField(max_length=50, null=True, blank=True)
    snapchat = models.CharField(max_length=50, null=True, blank=True)
