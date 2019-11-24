from django.db import models
from django.contrib.auth.models import User
from sgroups.models import Groups

# Create your models here.

class activity(models.Model):
    def __str__(self):
        if !(exp):
            return self.friend1.username+ " added " + self.friend2.username + " in " + self.group.name
        if self.group == "non-group":
            return self.friend1.username + " paid " + expense + " to " + self.friend2.username
        else:
            return self.friend1.username + " paid " + self.friend2.username + " in " + self.group.name

    friend1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend1')
	friend2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='friend2')
	# friend1 gives money to friend2
    exp = models.BooleanField()
    group = models.ForeignKey(Groups,on_delete=models.CASCADE,related_name='group')
	expense = models.DecimalField(decimal_places=2,default=0.0,max_digits=19)
