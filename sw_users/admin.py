from django.contrib import admin

# Register your models here.
from .models import CommonUser

admin.site.register(CommonUser)