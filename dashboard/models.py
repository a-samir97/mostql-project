from django.db import models
from users.models import AdminUser
# Create your models here.

class Logging(models.Model):

	user = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	action = models.CharField(max_length=30)


	def __str__(self):
		return self.user.username + " | " + self.action