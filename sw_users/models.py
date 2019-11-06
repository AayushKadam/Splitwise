from django.db import models

# Create your models here.

class CommonUser(models.Model):
    username = models.CharField(max_length=200,primary_key=True)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.username