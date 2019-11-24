from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class dost(models.Model):
	def __str__(self):
		return self.friend1.username + " " + self.friend2.username
	friend1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend1')
	friend2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend2')
	# friend2 gives money to friend1
	money = models.FloatField(default=0.0)


