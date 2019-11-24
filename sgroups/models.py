from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Groups(models.Model):
	def __str__ (self):
		return self.name
	name = models.CharField(max_length=100)

class Groupfriend(models.Model):
	def __str__(self):
		return self.friend1.username + " " + self.friend2.username
	groups = models.ForeignKey(Groups,on_delete=models.CASCADE,related_name='groups')
	friend1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='gfriend1')
	friend2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='gfriend2')
	# friend2 gives money to friend1
	money = models.FloatField(default=0.0)

class Groupmoney(models.Model):
	def __str__(self):
		return self.friend.username
	groups = models.ForeignKey(Groups,on_delete=models.CASCADE,related_name='ggroups')
	friend = models.ForeignKey(User,on_delete=models.CASCADE,related_name='gfriend')
	# friend2 gives money to friend1
	money = models.FloatField(default=0.0)