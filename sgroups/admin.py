from django.contrib import admin

from .models import Groups,Groupfriend,Groupmoney

# Register your models here.

admin.site.register(Groups)
admin.site.register(Groupfriend)
admin.site.register(Groupmoney)