from django.shortcuts import render
from sw_users.views import index as sind
from .models import activity
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def showactivity(request):
	if(request.user.is_anonymous):
		return sind(request)
	else:
		activities_related = [str(i) for i in activity.objects.filter(friend1 = request.user)]
		context = { 'activity_list' : reversed(activities_related) }
		return render(request,'activities/activity.html',context)
