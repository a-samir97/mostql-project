from django.db import models
from users.models import AdminUser
# Create your models here.

class Logging(models.Model):

	user = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	action = models.CharField(max_length=30)


	def __str__(self):
		return self.user.email + " | " + self.action

class Note(models.Model):
	
	title = models.CharField(max_length=50)
	description = models.TextField()
	url = models.CharField(max_length=120, null=True, blank=True)
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.title