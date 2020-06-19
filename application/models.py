from django.db import models

from users.models import AppUser

# status class 
# to get status of user 
# follow, add ,reject 
class Status(models.Model):
    action = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action

class UserStatus(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    status = models.ManyToManyField(Status)

# to get last 10 ip 
class UserIP(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()

# to get date of last 10 times sign in 
class LoginDates(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

# to get date of last 10 times account visited 
class VisitDates(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)